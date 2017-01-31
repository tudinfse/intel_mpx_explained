# ATTENTION: the tests are supposed to be run inside a container!
# all dependencies have to be installed before running the tests by `./entrypoint install -n benchmark_name`
from __future__ import absolute_import

import os
import subprocess

from core.environment import set_all_environments
from .abstract_test import BuildAndRun, current_action, current_benchmarks

set_all_environments()
os.environ['NUM_THREADS'] = '1'

COMP_BENCH = os.environ.get("COMP_BENCH")
CONF_DIR = "%s/experiments/makefiles" % COMP_BENCH
BUILD_DIR = "%s/experiments/build" % COMP_BENCH
DATA_PATH = os.environ.get("DATA_PATH")
INPUT_PATH = DATA_PATH + "/inputs/"


class Acceptance(BuildAndRun):
    # build types
    actions = {
        "gcc_native": (
            'gcc_mpx',
            'gcc_mpx_no_narrow_bounds',
            'gcc_mpx_only_write',
            'gcc_asan',
        ),
        "icc_native": (
            'icc_mpx',
            'icc_mpx_no_narrow_bounds',
            'icc_mpx_only_write',
        ),
        "clang_native": (
            'clang_asan',
            'clang_softbound',
            'clang_safecode'
        )
    }

    def test_01_builds(self):
        set_all_environments(env_type='build')
        benchmarks = current_benchmarks(self)
        actions = current_action(self)

        for name, params in benchmarks.items():
            for native, tested in actions.items():
                yield self.check_build, native, params[0]
                for t in tested:
                    yield self.check_build, t, params[0]

    def test_02_run(self):
        set_all_environments(env_type='both')
        benchmarks = current_benchmarks(self)
        actions = current_action(self)

        for name, params in benchmarks.items():
            for native, tested in actions.items():

                # run native and store output
                native_output = self.get_native_output(native, name, params[1])

                # run all tested types and compare outputs with native
                for t in tested:
                    yield self.compare_outputs, t, name, params[1], native_output

    def get_native_output(self, action, name, args):
        exe = BUILD_DIR + "/" + name + "/" + action + "/" + name
        run_command = exe + " " + args
        try:
            output = subprocess.check_output(run_command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(
                "\n    [[ RUN command failed with code %d]]\n    Command: %s\n" % (e.returncode, run_command))
            output = ""

        return output

    def compare_outputs(self, action, name, args, output_to_compare):
        exe = BUILD_DIR + "/" + name + "/" + action + "/" + name
        run_command = exe + " " + args

        try:
            output = subprocess.check_output(run_command, stderr=subprocess.STDOUT, shell=True)
            if output == output_to_compare:
                assert True
            else:
                assert False
        except subprocess.CalledProcessError as e:
            self.logger.error("\n    [[ RUN command failed with code %d]]\n    Command: %s\n" % (e.returncode, run_command))
            assert False
