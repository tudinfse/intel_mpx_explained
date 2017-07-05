import logging
import numpy as np

from core import prepare
from core import draw

BENCH_NAME = 'nginx'
EXP_NAME = BENCH_NAME
COMPILER_NAME = "long"


def main(t="perf"):
    logging.info("Processing data")
    df = prepare.process_results(t)
    if t == "tput":
        prepare.reorder_compilers(df, t)
        plot = draw.LinePlotTput()
        plot.get_data(df, [])
        plot.build_plot(
            # xlim=(0, 55),
            xticks=range(0, 100, 10),
            # ylim=(0.15, 0.72),
            yticks=np.arange(0.1, 1, 0.1),
        )
        plot.save_plot("nginx_%s.pdf" % t)

    else:
        logging.error("Unknown plot type")
        exit(-1)
