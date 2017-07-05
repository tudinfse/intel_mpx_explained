#!/usr/bin/env python
from __future__ import print_function

import logging
import os
import signal
from time import sleep
from subprocess import Popen, PIPE
import socket

from core.common_functions import *
from core.run import Runner


class NginxPerf(Runner):
    """
    Runs Nginx
    """

    name = "nginx"
    exp_name = "nginx"
    bench_suite = False

    benchmarks = {"nginx": ""}
    test_benchmarks = {"nginx": ""}
    client_numbers = [1, 5, 9, 13, 17, 21, 25, 29]
    ab = "ab"
    duration = 20  # in seconds
    requests_num = 1000000  # some huge number so we always take 20 seconds

    def __init__(self, *args, **kwargs):
        super(NginxPerf, self).__init__(*args, **kwargs)

        if self.config.input_type == "test":
            self.client_numbers = (1,)

    def per_benchmark_action(self, type_, benchmark, args):
        self.log_build(type_, benchmark)
        build_path = "/".join([self.dirs["build"], type_])
        self.current_exe = build_path + '/sbin/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['bench_src'],
            build_path=build_path
        )

        # generate an input file
        with open(build_path + "/html/index.html", "w") as f:
            f.write("<html><body><h1>It works!</h1>")
            random_text = my_check_output("lorem -p 10")
            f.write(random_text)
            f.write("</body></html>")

        # config Nginx
        replace_in_file(build_path + "/conf/nginx.conf", "listen       80;", "listen       8080;", ignoreifcontains=True)
        replace_in_file(build_path + "/conf/nginx.conf", "worker_processes  1;", "worker_processes  auto;", ignoreifcontains=True)

    def per_thread_action(self, type_, benchmark, args, thread_num):
        servercmd = "{action} {exe} -g \"daemon off;\"".format(
            action=self.action,
            exe=self.current_exe,
        )
        logging.debug("Server command: %s" % servercmd)

        # by default start client on local machine
        if env.get("CLIENT_MACHINE"):
            ssh = "ssh %s" % env["CLIENT_MACHINE"]
            logging.debug("Using remote client: %s" % env["CLIENT_MACHINE"])
        else:
            ssh = ""
            logging.debug("Using local client  (use CLIENT_MACHINE env var to specify remote client)")

        myip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

        with open(self.dirs["log_file"], "a") as f:
            for client_number in self.client_numbers:
                # start server
                my_check_output("pkill -9 nginx > /dev/null || true")  # for sanity
                sleep(1)
                server = Popen(servercmd, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
                sleep(1)

                # start client (possibly on another machine)
                msg = self.run_message.format(input=client_number, **locals())
                self.log_run(msg)
                f.write("[run] " + msg + "\n")

                out = my_check_output("{ssh} {ab} -k -t {duration} -n {requests_num} -c {client_number} http://{myip}:8080/".format(
                    ab=self.ab,
                    duration=self.duration,
                    requests_num=self.requests_num,
                    **locals()
                ))

                f.write("===== client =====\n")
                f.write(out)

                # log and stop server
                f.write("===== return code is %s =====\n" % str(server.poll()))
                try:
                    os.killpg(server.pid, signal.SIGINT)
                except:
                    pass
                f.write("===== stdout =====\n")
                for line in server.stdout:
                    f.write(line.decode('utf-8'))
                f.write("===== stderr =====\n")
                for line in server.stderr:
                    f.write(line.decode('utf-8'))
                sleep(1)

    def set_logging(self):
        self.num_benchmarks = len(self.benchmarks) * len(self.types) * self.num_runs * len(self.client_numbers)
        logging.info("Total runs: %d" % self.num_benchmarks)


def main(benchmark_name=None):
    runner = NginxPerf()
    runner.main()
