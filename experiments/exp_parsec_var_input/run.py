#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.runner import VarInputRunner


class ParsecVarInput(VarInputRunner):
    """
    Runs SPEC benchmarks
    """

    name = "parsec"
    exp_name = "parsec_var_input"
    bench_suite = True

    benchmarks = {
        "bodytrack": (
            "{input_dir}/sequenceB_261 4 5 16000  5 0 {thread}",
            "{input_dir}/sequenceB_261 4 5 32000  5 0 {thread}",
            "{input_dir}/sequenceB_261 4 5 64000  5 0 {thread}",
            "{input_dir}/sequenceB_261 4 5 128000 5 0 {thread}",
            "{input_dir}/sequenceB_261 4 5 256000 5 0 {thread}",
        ),
        "canneal": (
            "{thread} 15000 200 {input_dir}/103.nets 600",
            "{thread} 15000 200 {input_dir}/104.nets 600",
            "{thread} 15000 200 {input_dir}/105.nets 600",
            "{thread} 15000 200 {input_dir}/106.nets 600",
            "{thread} 15000 200 {input_dir}/107.nets 600",
        ),
        "streamcluster": (
            "10 20 64   100000 200 50000 none output.txt {thread}",
            "10 20 128  100000 200 50000 none output.txt {thread}",
            "10 20 256  100000 200 50000 none output.txt {thread}",
            "10 20 512  100000 200 50000 none output.txt {thread}",
            "10 20 1024 100000 200 50000 none output.txt {thread}",
        ),
        "blackscholes": (
            "{thread} {input_dir}/in400000.txt prices.txt",
            "{thread} {input_dir}/in800000.txt prices.txt",
            "{thread} {input_dir}/in1600000.txt prices.txt",
            "{thread} {input_dir}/in3200000.txt prices.txt",
            "{thread} {input_dir}/in6400000.txt prices.txt",
        ),
        "swaptions": (
            "-ns 512  -sm 10000 -nt {thread}",
            "-ns 1024 -sm 10000 -nt {thread}",
            "-ns 2048 -sm 10000 -nt {thread}",
            "-ns 4096 -sm 10000 -nt {thread}",
            "-ns 8192 -sm 10000 -nt {thread}",
        ),
    }

    def per_benchmark_action(self, type_, benchmark, args):
        build_path = "/".join([self.dirs["build"], benchmark, type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['suite_src'] + "/" + benchmark,
            build_path=build_path
        )


def main(benchmark_name=None):
    runner = ParsecVarInput(benchmark_name)
    runner.main()
