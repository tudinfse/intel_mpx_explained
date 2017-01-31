from __future__ import print_function

import logging
from os import environ as env
from abc import ABCMeta, abstractmethod, abstractproperty

from core.common_functions import c, my_check_output
from config import Config


class Runner:
    """
    Generic benchmark runner class
    """
    __metaclass__ = ABCMeta

    run_message = "name: {benchmark}; type: {type_}; threads: {thread_num}; input: {input};"

    def __init__(self, benchmark_name=''):
        self.benchmark_name = benchmark_name

        self.dirs = {}
        self.threads = []
        self.types = []
        self.action = ''
        self.num_runs = 0

        self.num_benchmarks = 0
        self.processed_benchmarks = 0

        self.current_args = ''
        self.current_exe = ''

        self.config = Config()

    # ===================
    # Abstract Properties
    # ===================
    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def exp_name(self):
        pass

    @abstractproperty
    def bench_suite(self):
        pass

    @abstractproperty
    def benchmarks(self):
        pass

    @abstractproperty
    def test_benchmarks(self):
        pass

    # ================
    # Main methods
    # ================
    def main(self):
        self.experiment_setup()
        self.experiment_loop()

    def experiment_setup(self):
        self.set_common_dirs()
        self.set_experiment_parameters()
        self.set_logging()

        self.remove_old_results([self.dirs["log_file"]])
        self.remove_old_build()

    def experiment_loop(self):
        for type_ in self.types:
            self.per_type_action(type_)

            for benchmark, args in self.benchmarks.items():
                self.per_benchmark_action(type_, benchmark, args)

                for i in range(0, self.num_runs):
                    self.per_run_action(i)

                    for thread_num in self.threads:
                        if not env.get("EXP_NO_RUN"):
                            self.per_thread_action(type_, benchmark, args, thread_num)

        self.clean()

    # =============================
    # Hooks for the experiment loop
    # =============================
    def per_run_action(self, i):
        pass

    def per_type_action(self, type_):
        pass

    def per_benchmark_action(self, type_, benchmark, args):
        pass

    def per_thread_action(self, type_, benchmark, args, thread_num):
        self.current_args = args.format(thread=thread_num, input_dir=self.dirs["input"] + '/' + benchmark)
        msg = self.run_message.format(input=self.config.input_type, **locals())
        real_threads = str(int(thread_num) - 1)

        with open(self.dirs["log_file"], "a") as f:
            self.log_run(msg)
            f.write("[run] " + msg + "\n")
            out = self.run(real_threads)
            f.write(out)
            f.write("[done]\n")

    def clean(self):
        pass

    # ==============
    # Common Methods
    # ==============
    def set_common_dirs(self):
        self.dirs = {
            "conf": env["COMP_BENCH"] + "/experiments/makefiles",
            "build": env["COMP_BENCH"] + "/experiments/build/" + self.name,
            "results": env["DATA_PATH"] + "/results/" + self.exp_name,
            "log_file": env["DATA_PATH"] + "/results/" + self.exp_name + "/" + self.exp_name + ".log",
            "libc": env["COMP_BENCH"] + "/src/util/libc",
            "input": env["DATA_PATH"] + "/inputs/" + self.name,
        }

        if self.bench_suite:
            env["BENCH_SUITE"] = self.name
            self.dirs["suite_src"] = env["COMP_BENCH"] + "/src/" + self.name
        else:
            self.dirs["bench_src"] = env["COMP_BENCH"] + "/src/applications/" + self.name

    def set_experiment_parameters(self):
        self.threads = env["NUM_THREADS"].split(" ")
        self.types = env["TYPES"].split(" ")
        self.action = env["STATS_ACTION"]
        self.num_runs = int(env["NUM_RUNS"])

        if self.config.input_type == "test":
            self.benchmarks = self.test_benchmarks

        if self.benchmark_name:
            self.benchmarks = (lambda x: {x: self.benchmarks[x]})(self.benchmark_name)

    def set_logging(self):
        self.num_benchmarks = len(self.benchmarks) * len(self.types)
        if not env.get("EXP_NO_RUN"):
            self.num_benchmarks = self.num_benchmarks * self.num_runs * len(self.threads)
        logging.info("Total runs: %d" % self.num_benchmarks)

    def remove_old_results(self, log_files):
        if not env.get("EXP_NO_RUN"):
            # remove old logs
            c("rm -rf " + self.dirs["results"])

            # create new (empty) ones
            c("mkdir -p " + self.dirs["results"])
            for f in log_files:
                c("touch " + f)

    def remove_old_build(self):
        if not env.get("EXP_NO_BUILD") and env.get("REBUILD"):
            c("rm -rf %s" % (self.dirs["build"]))

    def log_run(self, msg):
        logging.log(21, "[ {0:>4.1f}% ] {1}".format(self.processed_benchmarks * 100 / self.num_benchmarks, msg))
        self.processed_benchmarks += 1

    def run(self, real_threads):
        taskset = "taskset -c 0-{real_threads}".format(real_threads=real_threads)
        use_check_call = False

        if env.get('STATS_COLLECT') == 'mpxcount':
            # work-around issue of Intel Pin not working correctly with taskset and python inside Docker
            taskset    = ""
            use_check_call = True

        out = my_check_output("{action} {taskset} {exe} {args}".format(
            action=self.action,
            taskset=taskset,
            exe=self.current_exe,
            args=self.current_args,
            ),
            use_check_call)


        if env.get('STATS_COLLECT') == 'mpxcount':
            # collect statistics saved in mpxcount.tmp
            with open('mpxcount.tmp', 'r') as f:  out += "\n" + f.read()

        return out


class VarInputRunner(Runner):
    """
    Generic benchmark runner class (with varying inputs)
    """
    __metaclass__ = ABCMeta

    def per_thread_action(self, type_, benchmark, args_list, thread_num):
        for i, args in enumerate(args_list):
            self.current_args = args.format(thread=thread_num, input_dir=self.dirs["input"] + '/' + benchmark)
            msg = self.run_message.format(input=str(i), **locals())
            real_threads = str(int(thread_num) - 1)

            with open(self.dirs["log_file"], "a") as f:
                self.log_run(msg)
                f.write("[run] " + msg + "\n")
                out = self.run(real_threads)
                f.write(out)
                f.write("[done]\n")

    def set_logging(self):
        num_inputs = 5  # magic number for now (XS, S, M, L, XL)
        self.num_benchmarks = len(self.benchmarks) * len(self.types)
        if not env.get("EXP_NO_RUN"):
            self.num_benchmarks = self.num_benchmarks * self.num_runs * num_inputs
        logging.info("Total runs: %d" % self.num_benchmarks)
