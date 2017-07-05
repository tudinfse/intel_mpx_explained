#!/usr/bin/env python
from __future__ import print_function

import logging
import os
import signal
from time import sleep
from subprocess import Popen, PIPE

from core.common_functions import *
from core.runner import Runner


class NginxSecurity(Runner):
    """
    Test Nginx 1.4.0 against this bug:
        http://www.vnsecurity.net/research/2013/05/21/analysis-of-nginx-cve-2013-2028.html

    For the exploit script, you will probably need to install ruby+gem+ronin:
        apt-get install -y gem rubygems ruby-dev sqlite3 libsqlite3-dev && gem install ronin
    """

    name = "nginx"
    exp_name = "nginx_security"
    bench_suite = False

    benchmarks     = {"nginx": ""}
    ab             = "ab"

    def per_benchmark_action(self, type_, benchmark, args):
        build_path = "/".join([self.dirs["build"], type_])
        self.current_exe = build_path + '/sbin/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['bench_src'],
            build_path=build_path
        )

        # config Nginx
        replace_in_file(build_path + "/conf/nginx.conf", "listen       80;", "listen       8080;", ignoreifcontains=True)

    def per_thread_action(self, type_, benchmark, args, thread_num):
        servercmd = "strace -f {exe} -g \"daemon off;\"".format(exe=self.current_exe)
        logging.debug("Server command: %s" % servercmd)

        with open(self.dirs["log_file"], "a") as f:
            # start server
            my_check_output("pkill -9 nginx  > /dev/null || true")  # for sanity
            my_check_output("pkill -9 strace > /dev/null || true")  # for sanity
            sleep(1)
            server = Popen(servercmd, shell=True, stdout=PIPE, stderr=PIPE, preexec_fn=os.setsid)
            sleep(1)

            # start client
            msg = self.run_message.format(input="CVE-2013-2028", **locals())
            self.log_run(msg)

            f.write("******************************************************************************\n")
            f.write("[exploit] " + msg + "\n")
            f.write("******************************************************************************\n")

            my_check_output("ruby %s/CVE-2013-2028.rb 127.0.0.1 8080" % os.path.dirname(os.path.realpath(__file__)))
            sleep(1)

            # log and stop server
            f.write("===== return code is %s =====\n" % str(server.poll()))
            try:
                os.killpg(server.pid, signal.SIGKILL)
            except:
                pass
            f.write("===== error log =====\n")
            with open(os.path.dirname(self.current_exe) + "/../logs/error.log", "r") as errlog:
                for line in errlog.readlines():
                    f.write(line)
            f.write("===== stdout =====\n")
            for line in server.stdout:
                f.write(line.decode('utf-8'))
            f.write("===== stderr =====\n")
            for line in server.stderr:
                if "recv" in line.decode('utf-8'):
                    f.write(line.decode('utf-8'))
            sleep(1)

    def set_logging(self):
        self.num_benchmarks = len(self.benchmarks) * len(self.types) * self.num_runs
        logging.info("Total runs: %d" % self.num_benchmarks)


def main(benchmark_name=None):
    runner = NginxSecurity()
    runner.main()
