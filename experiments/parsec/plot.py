import logging
from pandas import Categorical

from core import prepare
from core import draw

BENCH_NAME = 'parsec'
EXP_NAME = BENCH_NAME
BENCHMARK_ORDER = (
    "blackscholes",
    "vips",
    "fluidanimate",
    "bodytrack",
    "ferret",
    "dedup",
    "facesim",
    "streamcluster",
    "raytrace",
    "x264",
    "canneal",
    "swaptions",
)
OVERFLOWS = {
    "perf": (
        # (11.0, 8.25, "12.6",),
    ),
    "mem": (
        (0.87, 6.25, "13.0",),
#        (1.53, 3.85, "4.98",),
#        (2.06, 3.85, "4.98",),
        (2.44, 6.25, "34.1",),
#        (3.87, 3.85, "4.65",),
#        (4.53, 3.85, "4.94",),
#        (5.07, 3.85, "5.84",),
#        (9.53, 4.25, "4.89",),
        (10.43, 8.25, "58.2",),
        (11.27, 8.25, "45",),
        (12.27, 8.25, "45",),
    ),
    "instr": (
#        (8.07,  4.25, "5.04",),
        (10.17, 8.25, "24.2",),
        (11.17, 8.25, "19.9",),
#        (12.17, 4.25, "8.06",),
    )
}


def process_type(t, df, plot_args, benchmark_order):
    columns = []

    # type specific processing
    if t == "perf":
        df = prepare.calculate_overhead(df)
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotOverhead()
        plot_args.update({
            "ylabel": "Normalized runtime\n(w.r.t. native)",
            "logy": True,
        })

    elif t == "mem":
        df = prepare.calculate_overhead(df, column="maxsize")
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotOverhead()
        plot_args.update({
            "ylabel": "Memory overhead\n(w.r.t. native)",
            "logy": True,
        })

    elif t == "multi":
        df = prepare.calculate_multithreading_overhead(df, over=2)
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        df["threads"] = Categorical(df["threads"], [8])
        df.sort_values(["threads"], inplace=True)

        plot = draw.BarplotMultithreaded()
        plot_args.update({
            "ylabel": "Speedup of 8 threads \nw.r.t. 2 threads",
            "ylim": (0.9, 4.5),
            "logy": True,
        })

    elif t == "cache":
        # values over 1000 instructions
        columns = ["l1_dcache_loads", "l1_dcache_load_misses", "l1_dcache_stores", "l1_dcache_store_misses",
                   "llc_loads", "llc_load_misses", "llc_stores", "llc_store_misses"]
        df = prepare.calculate_ratio(df, columns, "instructions")
        for c in columns:
            df[c] *= 100

        # differences
        df["L1 load hits"] = df["l1_dcache_loads"] - df["l1_dcache_load_misses"]
        df["LLC load hits"] = df["llc_loads"] - df["llc_load_misses"]
        df["L2 load hits"] = df["l1_dcache_load_misses"] - df["LLC load hits"]
        df["LLC load misses"] = df["llc_load_misses"]

        # df["l1_dcache_store_hits"] = df["l1_dcache_stores"] - df["l1_dcache_store_misses"]
        df["L1 store hits"] = df["l1_dcache_stores"] - df["llc_store_misses"]
        df["LLC store misses"] = df["llc_store_misses"]

        # ordering
        prepare.reorder_compilers(df, t)
        df = df.dropna(subset=['compilertype', 'name'])

        labels = df["compilertype"].unique()

        columns = ["L1 load hits", "L1 store hits",
                   "L2 load hits",
                   "LLC load hits", "LLC load misses", "LLC store misses"]

        plot = draw.BarplotClusteredStacked()
        plot_args.update({
            "ylabel": "Cache hits and misses\n(w.r.t. all instructions, %)",
            "xlabels": labels,
            "ylim": (0, 100),
            "yticks": range(0, 150, 20),
            "df_callback": prepare.reorder_and_rename_benchmarks,
            "df_callback_args": (benchmark_order,)
        })

    elif t == "instr":
        df = prepare.calculate_overhead(df, column="instructions")
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotOverhead()
        plot_args.update({
            "ylabel": "Instruction overhead\n(w.r.t. native)",
            "logy": True,
        })

    elif t == "misc_stat":
        # values over 1000 instructions
        columns = ["dtlb_stores", "dtlb_store_misses", "dtlb_load_misses", "dtlb_loads", "branch_misses",
                   "branch_instructions"]
        df = prepare.calculate_ratio(df, columns, "instructions")
        for c in columns:
            df[c] *= 100

        # differences
        df["dtlb_stores"] -= df["dtlb_store_misses"]
        df["dtlb_loads"] -= df["dtlb_load_misses"]
        df["branch_instructions"] -= df["branch_misses"]

        prepare.reorder_compilers(df, t)
        df = df.dropna(subset=['compilertype', 'name'])

        labels = df["compilertype"].unique()

        plot = draw.BarplotClusteredStacked()
        plot_args.update({
            "ylabel": "Other statistics\n(w.r.t. all instructions, %)",
            "xlabels": labels,
            "ylim": (0, 100),
            "yticks": range(0, 150, 20),
            "df_callback": prepare.reorder_and_rename_benchmarks,
            "df_callback_args": (benchmark_order,)
        })

    elif t == "ku_instr":
        df = prepare.calculate_overhead(df, column="instructions:k")
        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotOverhead()
        plot_args.update({
            "ylabel": "Kernel instruction overhead\n(w.r.t. native)",
            "logy": True,
        })

    elif t == "native_mem_access":
        # values over 1000 instructions
        columns = ["l1_dcache_loads", "l1_dcache_stores"]
        df = prepare.calculate_ratio(df, columns, "instructions")

        df["overhead"] = df["l1_dcache_loads"] + df["l1_dcache_stores"]
        df["overhead"] *= 100

        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotOverhead()
        plot_args.update({
            "ylabel": "Memory accesses\n(w.r.t. all instructions, %)",
            "ylim": (0, 115),
            "yticks": range(0, 101, 20),
        })

    elif t == "ipc":
        # IPC (instructions/cycle) is saved in "instructions" column
        df = prepare.calculate_ratio(df, ["instructions"], "cycles")
        df["overhead"] = df["instructions"]

        prepare.reorder_and_rename_benchmarks(df, benchmark_order)
        prepare.reorder_compilers(df, t)

        plot = draw.BarplotWithNative()
        plot_args.update({
            "ylabel": "Processor IPC\n(instructions/cycle)",
            "ylim": (0, 5.4),
            "yticks": range(0, 10, 1),
            "ncol": 6,
        })

    else:
        logging.error("Unknown plot type")
        exit(-1)

    # no need to return plot_args, dict is mutable and is passed by reference
    return plot, columns


def main(t="perf"):
    logging.info("Processing data")

    df = prepare.process_results(t)
    plot_args = {
        "ylim": (0.85, 10),
        "vline_position": 11.6,
        "title": "PARSEC",  # uncomment for web version
        "text_points": OVERFLOWS.get(t, ())
    }

    plot, columns = process_type(t, df, plot_args, BENCHMARK_ORDER)

    plot.get_data(df, columns)
    plot.build_plot(**plot_args)
    plot.save_plot("%s_%s.pdf" % (BENCH_NAME, t))
