# ATTENTION: the tests are supposed to be run inside a container!
# all dependencies have to be installed before running the tests by `./entrypoint install -n benchmark_name`
from .abstract_test import BuildAndRun, INPUT_PATH
from .abstract_acceptance_test import Acceptance
import sys
import logging
import unittest


class TestPhoenix(unittest.TestCase, BuildAndRun):
    # tested applications
    benchmarks = {
        # benchmark name: (path, test input)
        'histogram': ('src/phoenix_pthread/histogram', '%s/phoenix_pthread/histogram/input/small.bmp' % INPUT_PATH),
        'kmeans': ('src/phoenix_pthread/kmeans', ' '),
        'linear_regression': ('src/phoenix_pthread/linear_regression', '%s/phoenix_pthread/linear_regression/input/key_file_50MB.txt' % INPUT_PATH),
        'matrix_multiply': ('src/phoenix_pthread/matrix_multiply', '15 1'),
        'pca': ('src/phoenix_pthread/pca', '-r 30 -c 30'),
        'string_match': ('src/phoenix_pthread/string_match', '%s/phoenix_pthread/string_match/input/key_file_50MB.txt' % INPUT_PATH),
        'word_count': ('src/phoenix_pthread/word_count', '%s/phoenix_pthread/word_count/input/word_10MB.txt' % INPUT_PATH),
    }


class TestPhoenixAcceptance(TestPhoenix, Acceptance):
    pass

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
