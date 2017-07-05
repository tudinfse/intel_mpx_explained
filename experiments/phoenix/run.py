#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.run import Runner


class PhoenixPerf(Runner):
    """
    Runs Phoenix benchmarks
    """

    name = "phoenix"
    exp_name = "phoenix"
    bench_suite = True

    benchmarks = {
        "histogram": "{input_dir}/input/large.bmp",
        "kmeans": " ",
        "linear_regression": "{input_dir}/input/key_file_500MB.txt",
        "matrix_multiply": "1500 1",
        "pca": " -r 3000 -c 3000",
        "string_match": "{input_dir}/input/key_file_500MB.txt",
        "word_count": "{input_dir}/input/word_100MB.txt",
    }

    test_benchmarks = {
        "histogram": "{input_dir}/input/small.bmp",
        "kmeans": "-d 2 -c 10 -p 100 -s 100",
        "linear_regression": "{input_dir}/input/key_file_50MB.txt",
        "matrix_multiply": "15 1",
        "pca": " -r 30 -c 30",
        "string_match": "{input_dir}/input/key_file_50MB.txt",
        "word_count": "{input_dir}/input/word_10MB.txt",
    }

    def experiment_setup(self):
        self.set_common_dirs()
        self.set_experiment_parameters()
        self.set_logging()

        self.dirs['dry_run_log'] = self.dirs['results'] + "/phoenix_dry_run.log"
        self.remove_old_results([self.dirs["log_file"], self.dirs["dry_run_log"]])
        self.remove_old_build()

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

        args = args.format(input_dir=self.dirs["input"] + '/' + benchmark)

        # Dry run
        if not env.get("EXP_NO_RUN"):
            with open(self.dirs['dry_run_log'], "a") as f:
                f.write("--- Dry run for {benchmark} (input '{args}') ---\n".format(**locals()))
                out = my_check_output("{} {}".format(self.current_exe, args))
                f.write(out)


def main(benchmark_name=None):
    runner = PhoenixPerf(benchmark_name)
    runner.main()
