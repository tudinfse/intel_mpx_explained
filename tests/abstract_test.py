# ATTENTION: the tests are supposed to be run inside a container!
# all dependencies have to be installed before running the tests by `./entrypoint install -n benchmark_name`
from __future__ import absolute_import

import logging
import os
import subprocess

from core.environment import set_all_environments

set_all_environments()
os.environ['NUM_THREADS'] = '1'

COMP_BENCH = os.environ.get("COMP_BENCH")
CONF_DIR = "%s/experiments/makefiles" % COMP_BENCH
BUILD_DIR = "%s/experiments/build" % COMP_BENCH
DATA_PATH = os.environ.get("DATA_PATH")
INPUT_PATH = DATA_PATH + "/inputs/"


class BuildAndRun:
    # tested applications
    benchmarks = {}

    # build types
    actions = (
        'gcc_native',
        'gcc_mpx',
        'gcc_mpx_no_narrow_bounds',
        'gcc_mpx_only_write',
        'gcc_asan',

        'icc_native',
        'icc_mpx',
        'icc_mpx_no_narrow_bounds',
        'icc_mpx_only_write',

        'clang_native',
        'clang_asan',
        'clang_softbound',
    )

    logger = logging.getLogger("Test")

    def test_01_builds(self):
        set_all_environments(env_type='build')
        benchmarks = current_benchmarks(self)
        actions = current_action(self)

        for name, params in benchmarks.items():
            for action in actions:
                yield self.check_build, action, params[0]

    def test_02_run(self):
        set_all_environments(env_type='both')
        benchmarks = current_benchmarks(self)
        actions = current_action(self)

        for name, params in benchmarks.items():
            for action in actions:
                yield self.check_run, action, name, params[1]

    def check_build(self, action, path):
        threads = thread_num()
        make_command = 'make -j%s ACTION=%s -I %s -C %s' % (threads, action, CONF_DIR, path)
        try:
            output = subprocess.check_output(make_command, stderr=subprocess.STDOUT, shell=True)
            assert True
        except subprocess.CalledProcessError as e:
            self.logger.error("\n    [[ BUILD command failed ]]\n    Command: %s\n" % make_command)
            assert False

    def check_run(self, action, name, args):
        exe = BUILD_DIR + "/" + name + "/" + action + "/" + name
        run_command = exe + " " + args
        try:
            output = subprocess.check_output(run_command, stderr=subprocess.STDOUT, shell=True)
            assert True
        except subprocess.CalledProcessError as e:
            self.logger.error("\n    [[ RUN command failed with code %d]]\n    Command: %s\n" % (e.returncode, run_command))
            assert False


def current_benchmarks(obj):
    if os.environ.get("NAME"):
        benchmarks = (lambda x: {x: obj.benchmarks[x]})(os.environ.get("NAME"))
    else:
        benchmarks = obj.benchmarks

    return benchmarks


def current_action(obj):
    if os.environ.get("ACTION"):
        actions = (os.environ.get("ACTION"),)
    else:
        actions = obj.actions

    return actions


def thread_num():
    if os.environ.get("BUILD_THREADS_NUM"):
        threads = os.environ.get("BUILD_THREADS_NUM")
    else:
        threads = "1"

    return threads

