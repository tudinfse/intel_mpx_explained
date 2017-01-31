#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.runner import Runner
from collections import OrderedDict


class ParsecLibs(Runner):
    """
    Runs Parsec libs
    """

    name = "parsec_libs"
    exp_name = "parsec_libs"
    bench_suite = True

    benchmarks = OrderedDict()
    benchmarks['zlib']     = ""
    benchmarks['glib']     = ""
    benchmarks['gsl']      = ""
    benchmarks['libjpeg']  = ""
    benchmarks['libxml2']  = ""
    benchmarks['mesa']     = ""
    benchmarks['ssl']      = ""    # https://github.com/OleksiiOleksenko/mpx_evaluation/issues/36
    benchmarks['apr']      = ""
    benchmarks['apr-util'] = ""
    benchmarks['pcre']     = ""

    def per_benchmark_action(self, type_, benchmark, args):
        build_path = "/".join([self.dirs["build"], benchmark, type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['suite_src'] + "/" + benchmark,
            build_path=build_path
        )

    def per_thread_action(self, type_, benchmark, args, thread_num):
        # we don't want libs to be "performance-run"
        pass


def main(benchmark_name=None):
    runner = ParsecLibs(benchmark_name)
    runner.main()
