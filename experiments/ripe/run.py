#!/usr/bin/env python
from __future__ import print_function

import os

from core.common_functions import *
from core.runner import Runner


class RipeRunner(Runner):
    """
    RIPE tests using the authors' ripe_tester script
    """

    name = "ripe"
    exp_name = "ripe"
    bench_suite = False

    benchmarks = {"ripe": ""}

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
        servercmd = "{exe} -k start".format(exe=self.current_exe)
        logging.debug("Server command: %s" % servercmd)
        my_check_output("echo 0 > /proc/sys/kernel/randomize_va_space")

        with open(self.dirs["log_file"], "a") as f:
            msg = self.run_message.format(input="ripe", **locals())
            self.log_run(msg)
            f.write("[run] " + msg + "\n")
            # start ripe script
            out = my_check_output("python %s/ripe_tester.py %s both 1" %
                        (os.path.dirname(os.path.realpath(__file__)),
                         self.current_exe))
            f.write(out)
            f.write("[done]\n")


def main(benchmark_name=None):
    runner = RipeRunner()
    runner.main()
