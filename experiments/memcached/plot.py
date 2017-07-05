import logging
import numpy as np

from core import prepare
from core import draw


BENCH_NAME = 'memcached'
EXP_NAME = BENCH_NAME


def main(t="perf"):
    logging.info("Processing data")
    df = prepare.process_results(t)
    if t == "tput":
        df["lat"] /= 1000
        prepare.reorder_compilers(df, t)
        plot = draw.LinePlotTput()
        plot.get_data(df, [])
        plot.build_plot(
            xlim=(90, 290),
            xticks=range(100, 300, 50),
            ylim=(0.0, 3.0),
            yticks=np.arange(0.5, 3.0, 0.5),
            legend_loc='upper right'
        )
        plot.save_plot("memcached_%s.pdf" % t)

    else:
        logging.error("Unknown plot type")
        exit(-1)
