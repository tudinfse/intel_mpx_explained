import logging

from core import prepare
from ..parsec.plot import process_type

BENCH_NAME = 'phoenix'
EXP_NAME = BENCH_NAME
BENCHMARK_ORDER = (
    "linear_regression",
    "string_match",
    "matrix_multiply",
    "histogram",
    "kmeans",
    "pca",
    "word_count",

    # the following benchmarks are here for the case if want to make a combined plot
    # "blackscholes",
    # "vips",
    # "fluidanimate",
    # "bodytrack",
    # "ferret",
    # "dedup",
    # "facesim",
    # "streamcluster",
    # "raytrace",
    # "x264",
    # "canneal",
    # "swaptions",
    #
    # 'milc',
    # 'lbm',
    # 'gcc',
    # 'gobmk',
    # 'astar',
    # 'sphinx3',
    # 'bzip2',
    # 'libquantum',
    # 'mcf',
    # 'dealII',
    # 'hmmer',
    # 'namd',
    # 'sjeng',
    # 'omnetpp',
    # 'perlbench',
    # 'povray',
    # 'soplex',
    # 'h264ref',
    # 'xalancbmk',
)

OVERFLOWS = {
    "perf": (
       # (3.01, 8.3, "16.42",),
       # (6.01, 8.3, "11.53",),
    ),
    "mem": (
#        (3.97, 4.25, "5.31",),
    ),
    "instr": (
        (5.87, 4.25, "17.1",),
        (6.27, 4.25, "40.6",),
    )
}


def main(t="perf"):
    logging.info("Processing data")

    # common processing
    df = prepare.process_results(t)
    plot_args = {
        "ylim": (0.85, 10),
        "vline_position": 6.6,
        "title": "Phoenix",
        "text_points": OVERFLOWS.get(t, ())
    }
    plot, columns = process_type(t, df, plot_args, BENCHMARK_ORDER)

    if t == "multi":
        plot_args.update({
            "ylim": (0.51, 4.5),
        })

    plot.get_data(df, columns)
    plot.build_plot(**plot_args)
    plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))
