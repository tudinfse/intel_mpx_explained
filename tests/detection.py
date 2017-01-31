# ATTENTION: the tests are supposed to be run inside a container!
# all dependencies have to be installed before running the tests by `./entrypoint install -n benchmark_name`
from abstract_test import BuildAndRun, BUILD_DIR
import sys
import logging
import unittest
import subprocess

SRC_PATH = 'src/micro/acceptance/'


class TestDetection(BuildAndRun, unittest.TestCase):
    # tested applications
    benchmarks = {
        # benchmark name: (path, test input)
        'arbitrarycasts': (SRC_PATH + 'arbitrarycasts', ''),
        'globalarrayread': (SRC_PATH + 'globalarrayread', ''),
        'globalarraywrite': (SRC_PATH + 'globalarraywrite', ''),
        'malloc': (SRC_PATH + 'malloc', '2 10 1'),
        'multithreading': (SRC_PATH + 'multithreading', ''),
        'narrowing': (SRC_PATH + 'narrowing', ''),
        'stackarrayread': (SRC_PATH + 'stackarrayread', ''),
        'stackarraywrite': (SRC_PATH + 'stackarraywrite', ''),
    }

    def check_run(self, action, name, args):
        exe = BUILD_DIR + "/" + name + "/" + action + "/" + name
        run_command = exe + " " + args
        try:
            output = subprocess.check_output(run_command, stderr=subprocess.STDOUT, shell=True)
            self.logger.error(
                "\n    [[ The bug wasn't detected ]]\n    Command: %s\n" % run_command)
            assert False, "The bug wasn't detected"
        except subprocess.CalledProcessError as e:
            assert True

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
