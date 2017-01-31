import logging

from core import prepare
from ..exp_parsec_perf.plot import process_type

# === helpers === #
BENCH_NAME = 'phoenix'
EXP_NAME = '%s_perf' % BENCH_NAME
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
#        (4.07, 4.25, "4.52",),
#        (5.07, 4.25, "4.91",),
        (6.27, 8.25, "23.22",),
#        (7.27, 4.25, "4.98",),
    ),
    "mem": (
#        (3.97, 4.25, "5.31",),
    ),
    "instr": (
#        (2.55, 3.85, "4.87",),
#        (3.27, 3.85, "4.25",),
#        (4.75, 4.25, "6.50",),
#        (5.27, 4.25, "7.89",),
        (5.87, 8.25, "17.1",),
        (6.27, 8.25, "40.6",),
#        (6.87, 4.25, "4.53",),
#        (7.27, 4.25, "8.77",),
    )
}


def main(t="perf"):
    logging.info("Processing data")

    # common processing
    df = prepare.process_results(t)
    plot_args = {
        "ylim": (0.85, 10),
        "vline_position": 6.6,
        "title": "Phoenix",  # uncomment in web version
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
