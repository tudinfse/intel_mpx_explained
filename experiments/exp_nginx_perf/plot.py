import logging
import sys

import numpy as np
from pandas import Categorical

from core import prepare
from core import draw

# === helpers === #
BENCH_NAME = 'nginx'
EXP_NAME = '%s_perf' % BENCH_NAME
COMPILER_NAME = "long"

# NOTE 1: clang-asan performs ~15% better than clang-native!
# NOTE 2: icc-mpx performs ~7% better than icc-native!
# NOTE 3: native clang performs ~10% and icc ~18% worse than gcc!
def main(t="perf"):
    logging.info("Processing data")
    df = prepare.process_results(t)
    if t == "tput":
        prepare.reorder_compilers(df, t)
        plot = draw.LinePlotTput()
        plot.get_data(df, [])
        plot.build_plot(
            xlim=(0, 55),
            xticks=range(0, 100, 10),
            ylim=(0.15, 0.72),
            yticks=np.arange(0.1, 1, 0.1),
        )
        plot.save_plot("nginx_%s.pdf" % t)

    else:
        logging.error("Unknown plot type")
        exit(-1)
