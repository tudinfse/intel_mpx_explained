# ATTENTION: the tests are supposed to be run inside a container!
# all dependencies have to be installed before running the tests by `./entrypoint install -n benchmark_name`
from .abstract_test import BuildAndRun, INPUT_PATH
from .abstract_acceptance_test import Acceptance
import sys
import logging
import unittest


class TestParsec(unittest.TestCase, BuildAndRun):
    # tested applications
    benchmarks = {
        # benchmark name: (path, test input)
        'blackscholes': ('src/parsec/blackscholes', '1 %s/parsec/blackscholes/in_4.txt prices.txt' % INPUT_PATH),
        'bodytrack': ('src/parsec/bodytrack', '%s/parsec/bodytrack/sequenceB_1 4 1 4000 5 0 1' % INPUT_PATH),
        'canneal': ('src/parsec/canneal', '1 15000 2000 %s/parsec/canneal/10.nets 6000' % INPUT_PATH),
        'dedup': ('src/parsec/dedup', '-c -p -t 1 -i %s/parsec/dedup/test.dat -o output.dat.ddp' % INPUT_PATH),
        'facesim': ('src/parsec/facesim', '-timing -threads 1 -data_dir %s/parsec/facesim/test/' % INPUT_PATH),
        'ferret': ('src/parsec/ferret', '{0}/parsec/ferret/test/corel lsh {0}/parsec/ferret/test/queries 5 5 1 output.txt'.format(INPUT_PATH)),
        'fluidanimate': ('src/parsec/fluidanimate', '1 500 %s/parsec/fluidanimate/in_5K.fluid out.fluid' % INPUT_PATH),
        'raytrace': ('src/parsec/raytrace', '%s/parsec/raytrace/thai_statue.obj -automove -nthreads 1 -frames 20 -res 360 480' % INPUT_PATH),
        'streamcluster': ('src/parsec/streamcluster', '10 20 128 1000 200 5000 none output.txt 1'),
        'swaptions': ('src/parsec/swaptions', '-ns 128 -sm 100 -nt 1'),
        'vips': ('src/parsec/vips', 'im_benchmark %s/parsec/vips/barbados_256x288.v output.v' % INPUT_PATH),
        'x264': ('src/parsec/x264', '--quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads 1 -o eledream.264 %s/parsec/x264/eledream_32x18_1.y4m' % INPUT_PATH),
    }


class TestParsecAcceptance(TestParsec, Acceptance):
    pass

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
