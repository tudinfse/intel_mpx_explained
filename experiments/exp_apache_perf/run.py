#!/usr/bin/env python
from __future__ import print_function


import os
import signal
import logging
from os import environ as env
from time import sleep
from subprocess import Popen, PIPE
import socket

from core.common_functions import *
from core.runner import Runner


class ApachePerf(Runner):
    """
    Runs Apache
    """

    name = "apache"
    exp_name = "apache_perf"
    bench_suite = False

    benchmarks     = {"bin/httpd": ""}
    client_numbers = [1, 5, 9, 13, 17, 21, 25, 29, 31, 33, 35]
    ab             = "ab"
    duration       = 20     # in seconds
    requests_num   = 1000000 # some huge number so we always take 20 seconds

    if env.get("TESTRUN"):
        client_numbers = [1]

    def per_benchmark_action(self, type_, benchmark, args):
        build_path = "/".join([self.dirs["build"], type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['bench_src'],
            build_path=build_path
        )

        # modify httpd.conf
        # NOTE: we ignore SSL for perf experiment
#        replace_in_file(build_path + "/conf/httpd.conf", "#Include conf/extra/httpd-ssl.conf", "Include conf/extra/httpd-ssl.conf", ignoreifcontains=False)
#        replace_in_file(build_path + "/conf/extra/httpd-ssl.conf", "443", "8443", ignoreifcontains=True)
        replace_in_file(build_path + "/conf/httpd.conf", "Listen 80", "Listen 8080", ignoreifcontains=True)

        # random stuff
        c("openssl req -nodes -x509 -newkey rsa:2048 -keyout {0}/conf/server.key -out {0}/conf/server.crt -days 356 -subj \"/C=DE/ST=SN/L=NA/O=TU Dresden/OU=Org/CN=127.0.0.1\""
          .format(build_path))

        # generate an input file
        with open(build_path + "/htdocs/index.html", "w") as f:
            f.write("<html><body><h1>It works!</h1>")
            random_text = my_check_output("lorem -p 10")
            f.write(random_text)
            f.write("</body></html>")


    def per_thread_action(self, type_, benchmark, args, thread_num):
        servercmd = "{action} {exe} -k start -D FOREGROUND".format(
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
                my_check_output("pkill -9 httpd > /dev/null || true")  # for sanity
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
    runner = ApachePerf()
    runner.main()
