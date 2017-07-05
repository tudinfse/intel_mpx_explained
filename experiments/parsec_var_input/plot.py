import logging
from pandas import Categorical

from core import prepare
from core import draw


BENCH_NAME = 'parsec_var_input'
EXP_NAME = BENCH_NAME
BENCHMARK_ORDER = (
    "blackscholes",
    "streamcluster",
    "swaptions",
    "canneal",
)

OVERFLOWS = {
    "perf": (
        (-1.87, 8.25, "~12",),
    ),
    "mem": (
        (-10.07, 6.85, "21-26",),  # streamcluster
        (-4.87,  6.85, "9-26",),  # swaptions
    ),
}


def filter_inputs(df):
    df["input"] = Categorical(
        df["input"], [
            0,
            1,
            2,
        ],
        ordered=True
    )
    df.sort_values(["input"], inplace=True)


def process_type(t, df, plot_args, benchmark_order):
    if t == "perf":
        df = prepare.calculate_overhead(df, column="time")
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)
        filter_inputs(df)

        plot = draw.VarBarplotOverhead()
        plot_args.update({
            "ylabel": "Normalized runtime\n(w.r.t. native)",
            "logy": True,
        })

    elif t == "mem":
        df = prepare.calculate_overhead(df, column="maxsize")
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)
        filter_inputs(df)

        plot = draw.VarBarplotOverhead()
        plot_args.update({
            "ylabel": "Memory overhead\n(w.r.t. native)",
            "logy": True,
        })

    return plot, []


def main(t="perf"):
    logging.info("Processing data")

    # common processing
    df = prepare.process_results(t)
    plot_args = {
        "ylim": (0.8, 10),
        "vline_position": 11.6,
        "title": "PARSEC",
        "text_points": OVERFLOWS.get(t, ())
    }
    plot, columns = process_type(t, df, plot_args, BENCHMARK_ORDER)

    plot.get_data(df, columns)
    plot.build_plot(**plot_args)
    plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))
