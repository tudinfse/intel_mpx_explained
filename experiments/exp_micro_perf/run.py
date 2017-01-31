#!/usr/bin/env python
from __future__ import print_function

from core.common_functions import *
from core.runner import Runner


class MicroPerf(Runner):
    """
    Runs micro benchmarks
    """

    name = "micro/perf/"
    exp_name = "micro_perf"
    bench_suite = True

    benchmarks = {
        "arrayread": "",
        "arraywrite": "",
        # "funccalls": "",
        "mallocs": "",
        "multithreading_fp": "",
        "multithreading_fn": "",
        "struct": "",
        "ptrcreation": "",
    }

    def experiment_setup(self):
        self.set_common_dirs()
        self.set_experiment_parameters()
        self.set_logging()

        self.dirs['dry_run_log'] = self.dirs['results'] + "/micro_perf_dry_run.log"
        self.remove_old_results([self.dirs["log_file"], self.dirs["dry_run_log"]])
        self.remove_old_build()

    def per_benchmark_action(self, type_, benchmark, args):
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
    runner = MicroPerf(benchmark_name)
    runner.main()
