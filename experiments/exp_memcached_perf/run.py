#!/usr/bin/env python
from __future__ import print_function

import logging
import os
import signal
from time import sleep
from subprocess import Popen, PIPE
import socket

from core.common_functions import *
from core.runner import Runner


class MemcachedPerf(Runner):
    """
    Runs Memcached with Memaslap client
    """

    name = "memcached"
    exp_name = "memcached_perf"
    bench_suite = False

    benchmarks = {"bin/memcached": ""}
    client_numbers = (32, 64, 128, 192, 256, 320, 384, 448, 512)
    memaslap       = "memaslap"
    duration       = 20     # in seconds

    if env.get("TESTRUN"):
        client_numbers = [32]

    def per_benchmark_action(self, type_, benchmark, args):
        build_path = "/".join([self.dirs["build"], type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['bench_src'],
            build_path=build_path
        )

    def per_thread_action(self, type_, benchmark, args, thread_num):
        # currently: always use 8 threads
        servercmd = "{action} {exe} -p 8080 -t 8 -u root".format(
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
                my_check_output("pkill -9 memcached > /dev/null || true")  # for sanity
                sleep(1)
                server = Popen(servercmd, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
                sleep(1)

                # start client (possibly on another machine)
                msg = self.run_message.format(input=client_number, **locals())
                self.log_run(msg)
                f.write("[run] " + msg + "\n")

                out = my_check_output("{ssh} {memaslap} -s {myip}:8080 -t {duration}s -c {client_number} -T 8 -S {duration}s".format(
                    memaslap=self.memaslap,
                    duration=self.duration,
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
    runner = MemcachedPerf()
    runner.main()
