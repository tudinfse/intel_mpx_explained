#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.run import Runner


class ParsecPerf(Runner):
    """
    Runs Parsec benchmarks
    """

    name = "parsec"
    exp_name = "parsec"
    bench_suite = True

    benchmarks = {
        "blackscholes": "{thread} {input_dir}/in_10M.txt prices.txt",
        "bodytrack": "{input_dir}/sequenceB_261 4 261 4000 5 0 {thread}",
        "canneal": "{thread} 15000 2000 {input_dir}/2500000.nets 6000",
        "dedup": "-c -p -t {thread} -i {input_dir}/FC-6-x86_64-disc1.iso -o output.dat.ddp",
        "facesim": "-timing -threads {thread} -data_dir {input_dir}/dev",
        "ferret": "{input_dir}/corel lsh {input_dir}/queries 50 20 {thread} output.txt",
        "fluidanimate": "{thread} 500 {input_dir}/in_500K.fluid out.fluid",
        "raytrace": "{input_dir}/thai_statue.obj -automove -nthreads {thread} -frames 200 -res 1920 1080",
        "streamcluster": "10 20 128 1000000 200000 5000 none output.txt {thread}",
        "swaptions": "-ns 128 -sm 1000000 -nt {thread}",
        "vips": "im_benchmark {input_dir}/orion_18000x18000.v output.v",
        "x264": "--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs " +
                "--no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads {thread} " +
                "-o eledream.264 {input_dir}/eledream_1920x1080_512.y4m",
    }

    test_benchmarks = {
        "blackscholes": "{thread} {input_dir}/in_4.txt prices.txt",
        "bodytrack": "{input_dir}/sequenceB_1 4 1 4000 5 0 {thread}",
        "canneal": "{thread} 15000 2000 {input_dir}/10.nets 6000",
        "dedup": "-c -p -t {thread} -i {input_dir}/test.dat -o output.dat.ddp",
        "facesim": "-timing -threads {thread} -data_dir {input_dir}/test/",
        "ferret": "{input_dir}/test/corel lsh {input_dir}/test/queries 5 5 {thread} output.txt",
        "fluidanimate": "{thread} 500 {input_dir}/in_5K.fluid out.fluid",
        "raytrace": "{input_dir}/thai_statue.obj -automove -nthreads {thread} -frames 20 -res 360 480",
        "streamcluster": "10 20 128 1000 200 5000 none output.txt {thread}",
        "swaptions": "-ns 128 -sm 100 -nt {thread}",
        "vips": "im_benchmark {input_dir}/barbados_256x288.v output.v",
        "x264": "--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs " +
                "--no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads {thread} " +
                "-o eledream.264 {input_dir}/eledream_32x18_1.y4m",
    }

    def per_benchmark_action(self, type_, benchmark, args):
        self.log_build(type_, benchmark)
        build_path = "/".join([self.dirs["build"], benchmark, type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['suite_src'] + "/" + benchmark,
            build_path=build_path
        )

    def per_thread_action(self, type_, benchmark, args, thread_num):
        # VIPS expects the number of threads in an environment variable
        # we set this envvar for everything, to be on the safe side
        env["IM_CONCURRENCY"] = thread_num
        super(ParsecPerf, self).per_thread_action(type_, benchmark, args, thread_num)


def main(benchmark_name=None):
    runner = ParsecPerf(benchmark_name)
    runner.main()
