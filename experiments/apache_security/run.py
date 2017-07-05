#!/usr/bin/env python
from __future__ import print_function

import os
import signal
import logging
from time import sleep
from subprocess import Popen, PIPE

from core.common_functions import *
from core.runner import Runner


class ApacheSecurity(Runner):
    """
    Test Apache with vulnerable OpenSSL 1.0.1f against Heartbleed bug:
        http://www.theregister.co.uk/2014/04/09/heartbleed_explained/
    """

    name = "apache"
    exp_name = "apache_security"
    bench_suite = False

    benchmarks     = {"bin/httpd": ""}

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
        replace_in_file(build_path + "/conf/httpd.conf", "#Include conf/extra/httpd-ssl.conf", "Include conf/extra/httpd-ssl.conf", ignoreifcontains=False)
        replace_in_file(build_path + "/conf/extra/httpd-ssl.conf", "443", "8443", ignoreifcontains=True)
        replace_in_file(build_path + "/conf/httpd.conf", "Listen 80", "Listen 8080", ignoreifcontains=True)

        # random stuff
        c("openssl req -nodes -x509 -newkey rsa:2048 -keyout {0}/conf/server.key -out {0}/conf/server.crt -days 356 -subj \"/C=DE/ST=SN/L=NA/O=TU Dresden/OU=Org/CN=127.0.0.1\""
          .format(build_path))

    def per_thread_action(self, type_, benchmark, args, thread_num):
        servercmd = "{exe} -k start".format(exe=self.current_exe)
        logging.debug("Server command: %s" % servercmd)

        with open(self.dirs["log_file"], "a") as f:
            for paylength in ["0x8000", "0xF000"]:
                f.write("========== payload length is %s ==========\n" % paylength)

                # start server
                my_check_output("pkill -9 httpd > /dev/null || true")  # for sanity
                sleep(1)
                server = Popen(servercmd, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
                sleep(1)

                # start client (possibly on another machine)
                msg = self.run_message.format(input="heartbleed", **locals())
                self.log_run(msg)
                f.write("******************************************************************************\n")
                f.write("[exploit] " + msg + "\n")
                f.write("******************************************************************************\n")

                # start ab in background (to create confidential payload)
                my_check_output("ab -k -t 20 -c 20 -H CONFIDENTIAL_DATA https://127.0.0.1:8443/ > /dev/null 2>&1 &")
                sleep(5)

                out = my_check_output("python %s/heartbleed.py 127.0.0.1 -p 8443 -n 5 -l %s" % (os.path.dirname(os.path.realpath(__file__)), paylength))
                f.write("===== exploit output =====\n")
                f.write(out)

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

                my_check_output("pkill -9 ab > /dev/null || true")
                my_check_output("pkill -9 httpd > /dev/null || true")  # for sanity
                sleep(1)

    def set_logging(self):
        self.num_benchmarks = len(self.benchmarks) * len(self.types) * self.num_runs * 2
        logging.info("Total runs: %d" % self.num_benchmarks)


def main(benchmark_name=None):
    runner = ApacheSecurity()
    runner.main()
