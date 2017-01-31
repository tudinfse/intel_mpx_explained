import logging

from pandas import Categorical

from core import prepare
from ..exp_parsec_var_input.plot import process_type

# === helpers === #
BENCH_NAME = 'phoenix_var_input'
BENCHMARK_ORDER = (
    "linear_regression",
    "string_match",
    "matrix_multiply",
    # "histogram",
    # "kmeans",
    # "pca",
    "word_count"
)

OVERFLOWS = {
    "perf": (
        (3.07, 6.85, "13-25",),
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


def main(t="perf"):
    logging.info("Processing data")

    # common processing
    df = prepare.process_results(t)
    plot_args = {
        "ylim": (0.8, 10),
        "vline_position": 11.6,
        "title": "Phoenix",  # uncomment in web version
        "text_points": OVERFLOWS.get(t, ())
    }
    plot, columns = process_type(t, df, plot_args, BENCHMARK_ORDER)

    if t=="mem":
        plot_args.update({
            "ylim": (0.65, 10),
        })

    plot.get_data(df, columns)
    plot.build_plot(**plot_args)
    plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))
