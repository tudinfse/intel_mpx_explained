#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.runner import VarInputRunner


class PhoenixVarInput(VarInputRunner):
    """
    Runs Phoenix benchmarks with varying inputs
    """

    name = "phoenix_pthread"
    exp_name = "phoenix_var_input"
    bench_suite = True

    benchmarks = {
        "kmeans": (
            " -p 400000 -c 2",
            " -p 800000 -c 2",
            " -p 1600000 -c 2",
            " -p 3200000 -c 2",
            " -p 6400000 -c 2",
        ),
        "linear_regression": (
            "{input_dir}/input/key_file_50MB.txt",
            "{input_dir}/input/key_file_100MB.txt",
            "{input_dir}/input/key_200MB.txt",  # touch key_200MB.txt; for i in 1 2; do cat key_file_100MB.txt >> key_200MB.txt; done;
            "{input_dir}/input/key_400MB.txt",  # touch key_400MB.txt; for i in 1 2 3 4; do cat key_file_100MB.txt >> key_400MB.txt; done;
            "{input_dir}/input/key_800MB.txt",  # touch key_800MB.txt; for i in 1 2 3 4 5 6 7 8; do cat key_file_100MB.txt >> key_800MB.txt; done;
        ),
        "matrix_multiply": (
            "325 1",
            "750 1",
            "1500 1",
            "3000 1",
            "6000 1",
        ),
        "pca": (
            " -r 325 -c 3000",
            " -r 750 -c 3000",
            " -r 1500 -c 3000",
            " -r 3000 -c 3000",
            " -r 6000 -c 3000",
        ),
        "string_match": (
            "{input_dir}/input/key_file_50MB.txt",
            "{input_dir}/input/key_file_100MB.txt",
            "{input_dir}/input/key_200MB.txt",  # touch key_200MB.txt; for i in 1 2; do cat key_file_100MB.txt >> key_200MB.txt; done;
            "{input_dir}/input/key_400MB.txt",  # touch key_400MB.txt; for i in 1 2 3 4; do cat key_file_100MB.txt >> key_400MB.txt; done;
            "{input_dir}/input/key_800MB.txt",  # touch key_800MB.txt; for i in 1 2 3 4 5 6 7 8; do cat key_file_100MB.txt >> key_800MB.txt; done;
        ),
        "word_count": (
            "{input_dir}/input/word_10MB.txt",
            "{input_dir}/input/word_50MB.txt",
            "{input_dir}/input/word_100MB.txt",
            "{input_dir}/input/key_200MB.txt",  # touch key_200MB.txt; for i in 1 2; do cat word_100MB.txt >> key_200MB.txt; done;
            "{input_dir}/input/key_400MB.txt",  # touch key_400MB.txt; for i in 1 2 3 4; do cat word_100MB.txt >> key_400MB.txt; done;
        ),
    }

    def experiment_setup(self):
        self.set_common_dirs()
        self.set_experiment_parameters()
        self.set_logging()

        self.dirs['dry_run_log'] = self.dirs['results'] + "/phoenix_perf_dry_run.log"
        self.remove_old_results([self.dirs["log_file"], self.dirs["dry_run_log"]])
        self.remove_old_build()

    def per_benchmark_action(self, type_, benchmark, args_list):
        build_path = "/".join([self.dirs["build"], benchmark, type_])
        self.current_exe = build_path + '/' + benchmark

        build_benchmark(
            b=benchmark,
            t=type_,
            makefile=self.dirs['suite_src'] + "/" + benchmark,
            build_path=build_path
        )

        args = args_list[0].format(input_dir=self.dirs["input"] + '/' + benchmark)

        # Dry run
        if not env.get("EXP_NO_RUN"):
            with open(self.dirs['dry_run_log'], "a") as f:
                f.write("--- Dry run for {benchmark} (input '{args}') ---\n".format(**locals()))
                out = my_check_output("{} {}".format(self.current_exe, args))
                f.write(out)


def main(benchmark_name=None):
    runner = PhoenixVarInput(benchmark_name)
    runner.main()
