import logging
import sys

import matplotlib.pyplot as plt
import numpy as np
from pandas import Categorical

from core import prepare
from core import draw

# === helpers === #
BENCH_NAME = 'mergedplots'
EXP_NAME = BENCH_NAME

BENCHMARK_ORDER = (
    "smatch",
    "matrixmul",
    "wordcnt",

    "blackscholes",
    "facesim",
    "swaptions",

    "bz2",
    "mcf",
    "perlbmk",
)

def prepare_specific(name, df):
    if "memcached" in name:
        df["lat"] /= 1000


def limits_specific(name):
    if "memcached" in name:
        return {
            "xlim"  : (90, 310),
            "xticks": range(100, 320, 50),
            "ylim"  : (0.0, 3.0),
            "yticks": np.arange(0.5, 3.0, 0.5),
        }
    if "apache" in name or "httpd" in name:
        return {
            "xlim"  : (-2, 54),
            "xticks": range(0, 60, 10),
            "ylim"  : (0.42, 0.92),
            "yticks": np.arange(0.1, 1, 0.1),
        }
    if "nginx" in name:
        return {
            "xlim"  : (-2, 54),
            "xticks": range(0, 60, 10),
            "ylim"  : (0.15, 0.72),
            "yticks": np.arange(0.1, 1, 0.1),
        }
    return {
        "xlim"  : None,
        "xticks": None,
        "ylim"  : None,
        "yticks": None,
    }

OVERFLOWS = {
    "perf": (
        (5.28, 6.25, "23.22",),
        (8.16, 8.25, "12.6",),
        (11.19, 8.25, "28.8",),
    ),
    "mem": (
        (1.28, 6.25, "45",),
        (7.44, 8.25, "58.2",),
        (8.28, 8.25, "45",),
    ),
    "instr": (
        (4.46, 6.25, "17.1",),
        (5.28, 6.25, "40.6",),
        (8.18, 8.25, "19.9",),
        (11.18, 8.25, "22.9",),
    )
}


def main(t="tput"):
    logging.info("Processing data")
    if t == "tput":
        df = prepare.process_results(t)

        # NOTE: specific names and order
        names  = ["bin/httpd", "nginx", "bin/memcached"] # df["name"].unique()
        titles = ["Apache", "Nginx", "Memcached"] # df["name"].unique()
        idxs   = ["(a)", "(b)", "(c)"]

        fig = plt.figure()
        plot = draw.LinePlotTput()

        for idx, name in enumerate(names):
            sub = fig.add_subplot(1, len(names), idx+1)
            dff = df[df["name"] == name].copy()
            prepare_specific(name, dff)

            # NOTE 1: since all compilers perform roughly the same, we leave gcc only for simplicity
            prepare.reorder_compilers(dff, t)
            limits = limits_specific(name)

            plot.get_data(dff, [])

            xlabel = " "
            ylabel = ""
            if idx == 1: xlabel = r"Throughput ($\times 10^3$ msg/s)"
            if idx == 0: ylabel = r"Latency (ms)"

            plot.build_plot(
                xlabel=xlabel,
                ylabel=ylabel,
                subplot=sub,
                xlim=limits["xlim"],
                xticks=limits["xticks"],
                ylim=limits["ylim"],
                yticks=limits["yticks"],
                figsize=(12, 3),
            )
            subplot = plot.get_current_subplot()

            subplot.text(0.5, 1.02, idxs[idx] + " " + titles[idx], fontsize=12, horizontalalignment='center', transform=subplot.transAxes)
            for showlegendname in ["nginx"]:
                if showlegendname not in name:
                    subplot.legend().set_visible(False)

        plot.save_plot(filename="merged_%s.pdf" % t)

    elif t == "perf":
        plot_args = {
            "ylabel": "Normalized runtime\n(w.r.t. native)",
            "ylim": (0.85, 10),
            "vline_position": 2.5,
            "logy": True,
            "text_points": OVERFLOWS.get(t, ())
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotOverhead()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "mem":
        plot_args = {
            "ylabel": "Memory overhead\n(w.r.t. native)",
            "ylim": (0.85, 10),
            "vline_position": 2.5,
            "logy": True,
            "text_points": OVERFLOWS.get(t, ())
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotOverhead()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "mpxcount":
        (file_name, df) = prepare.read_raw()
        prepare.reorder_compilers(df, t)
        labels = df["compilertype"].unique()
        plot_args = {
            "ylabel": "MPX instructions\n(w.r.t. all instructions, %)",
            "xlabels": labels,
            "ylim": (0, 52),
            "yticks": range(0, 90, 10),
            "df_callback": prepare.reorder_and_rename_benchmarks,
            "df_callback_args": (BENCHMARK_ORDER,)
        }
        plot = draw.BarplotClusteredStacked()
        plot.columns = ["bndcl", "bndcu", "bndldx", "bndstx", "bndmovreg", "bndmovmem"]
        plot.df = df
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "multi":
        plot_args = {
            "ylabel": "Speedup of 8 threads \nw.r.t. 2 threads",
            "ylim": (0.51, 4.5),
            "vline_position": 1.5,
            "logy": True,
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotMultithreaded()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "cache":
        (file_name, df) = prepare.read_raw()
        prepare.reorder_compilers(df, t)
        labels = df["compilertype"].unique()
        plot_args = {
            "ylabel": "Cache hits and misses\n(w.r.t. all instructions, %)",
            "xlabels": labels,
            "ylim": (0, 100),
            "yticks": range(0, 150, 20),
            "df_callback": prepare.reorder_and_rename_benchmarks,
            "df_callback_args": (BENCHMARK_ORDER,)
        }
        plot = draw.BarplotClusteredStacked()
        plot.columns = ["L1 load hits", "L1 store hits", "L2 load hits",
                   "LLC load hits", "LLC load misses", "LLC store misses"]
        plot.df = df
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "instr":
        plot_args = {
            "ylabel": "Instruction overhead\n(w.r.t. native)",
            "ylim": (0.85, 10),
            "vline_position": 2.5,
            "logy": True,
            "text_points": OVERFLOWS.get(t, ())
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotOverhead()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "ipc":
        plot_args = {
            "ylabel": "Processor IPC\n(instructions/cycle)",
            "ylim": (0, 5.4),
            "vline_position": 2.5,
            "yticks": range(0, 10, 1),
            "ncol": 6,
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotWithNative()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "mpx_feature_perf":
        plot_args = {
            "ylabel": "Normalized runtime\n(w.r.t. native)",
            "ylim": (0.85, 10),
            "vline_position": 2.5,
            "build_names": "mpx_feature",
            "logy": True,
            "ncol": 6,
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotMPXFature()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    elif t == "mpx_feature_mem":
        plot_args = {
            "ylabel": "Memory overhead\n(w.r.t. native)",
            "ylim": (0.85, 10),
            "vline_position": 2.5,
            "build_names": "mpx_feature",
            "logy": True,
            "ncol": 6,
        }
        (file_name, df) = prepare.read_raw()
        plot = draw.BarplotMPXFature()
        plot.df = df
        plot.df = plot.df.set_index("name")
        plot.build_plot(**plot_args)
        plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))

    else:
        logging.error("Unknown plot type")
        exit(-1)
