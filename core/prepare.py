import os
from collections import defaultdict, OrderedDict

from pandas import read_csv, DataFrame, Categorical, Series
import numpy as np
from scipy.stats import trim_mean
from scipy.stats.mstats import mode, gmean, hmean

import logging


# taken from http://stackoverflow.com/questions/27424178/faster-way-to-remove-outliers-by-group-in-large-pandas-dataframe
def winsorize_series(s, fields_to_aggregate):
    if s.name not in fields_to_aggregate:
        return s
    q = s.quantile([0.05, 0.95])
    if isinstance(q, Series) and len(q) == 2:
        s[s < q.iloc[0]] = q.iloc[0]
        s[s > q.iloc[1]] = q.iloc[1]
    return s


def winsorize_df(df, fields_to_aggregate):
    print(fields_to_aggregate)
    print(df)
    exit(1)
    return df.apply(winsorize_series, fields_to_aggregate=fields_to_aggregate)


def cvpct(s):
    """ Coefficient of Variation (in percentages) """
    m = np.mean(s)
    if np.isnan(m) or m == 0.0:
        return np.nan
    return 100.0*np.std(s)/m


def check_overhead(row):
    MIN_OVERHEAD_POSSIBLE = 0.5
    if row["overhead"] < MIN_OVERHEAD_POSSIBLE:
        logging.warning("Detected overhead less than " + str(MIN_OVERHEAD_POSSIBLE) + " in row:\n" + str(row))
        row["overhead"] = float('nan')


def read_raw():
    if os.environ["PLOT_FILE"]:
        file_name = os.environ["PLOT_FILE"]
    else:
        logging.error("File name of an input file is not set")
        exit(1)

    try:
        df = read_csv(file_name)
        os.chdir(os.path.dirname(file_name))
    except:
        logging.error("File %s not found or is not a correct csv file" % (file_name))
        exit(1)

    return (file_name, df)


def process_results(t="perf"):
    """
    Calculate mean values and do other required processing of the raw data
    :param t: experiment type
    :return: DataFrame with processed data
    """
    # TODO: revert back to using `cycles` instead of `time` when we fix the bug with BigIntegers
    columns = {
        # type: (what to aggregate, what to keep)
        "perf": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "multi": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "perfstacked": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "mem": (["maxsize"], ["compiler", "type", "name", "input", "threads"]),
        "tput": (["tput", "lat"], ["compiler", "type", "name", "num_clients", "input", "threads"]),
        "instr": (["instructions"], ["compiler", "type", "name", "input", "threads"]),
        "mpxcount": (
            ["bndldx", "bndstx", "bndmovreg", "bndmovmem", "bndcu", "bndmk", "bndcl", "instructions", "memory_reads", "memory_writes"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "cache": (
            ["instructions", "l1_dcache_loads", "l1_dcache_load_misses", "l1_dcache_stores", "l1_dcache_store_misses", "llc_loads", "llc_load_misses", "llc_stores", "llc_store_misses"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "misc_stat": (
            ["instructions", "dtlb_stores", "dtlb_store_misses", "dtlb_load_misses", "dtlb_loads", "branch_misses", "branch_instructions"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "ku_instr": (
            ["instructions", "instructions:u", "instructions:k"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "native_mem_access": (
            ["instructions", "l1_dcache_loads", "l1_dcache_stores"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "ipc": (
            ["instructions", "cycles"],
            ["compiler", "type", "name", "input", "threads"]
        ),
        "mpx_feature_perf": (["time"], ["compiler", "type", "name", "input", "threads"]),
        "mpx_feature_mem": (["maxsize"], ["compiler", "type", "name", "input", "threads"]),
    }

    # get raw data
    (file_name, df) = read_raw()

    # calculate mean values
    fields_to_aggregate = columns[t][0]
    fields_to_keep = columns[t][1]
#    df = df.groupby(fields_to_keep).apply(winsorize_df, fields_to_aggregate=fields_to_aggregate)

    df.groupby(fields_to_keep).agg([np.mean, np.std, cvpct, np.count_nonzero]).to_csv(file_name + ".stats.csv")

    df = DataFrame(
        # it's dictionary comprehension, in case you're wondering
        {k: df.groupby(fields_to_keep)[k].mean() for k in fields_to_aggregate}
#        {k: df.groupby(fields_to_keep)[k].apply(gmean, axis=None) for k in fields_to_aggregate}
    )

    # from grouped table to normal DataFrame
    df = df.reset_index()

    if t == "mem":
        # from KB -> MB
        df["maxsize"] /= 1000
    if t == "tput":
        # from messages -> thousands of messages
        df["tput"] /= 1000

    # merge compiler-type for convience
    df["compilertype"] = df["compiler"] + "-" + df["type"]

    return df


def calculate_overhead(df, column="time", over_compilertype=None, over_column=None):
    """
    Calculate overheads for all build types.
    If `over` is not given, overhead is calculated over `native` build type.
    :param df: DataFrame to be processed
    :param column: which column to process
    :param over_compilertype: which build type to use as baseline (e.g., "gcc-native")
    :return: processed DataFrame
    """

    # initialize
    df["overhead"] = 0

    # define aggregation parameters
    native_column = over_column if over_column else column
    type_column = "compilertype" if over_compilertype else "type"
    native_type = over_compilertype if over_compilertype else "native"

    # do the calculation
    for i, row in df.iterrows():
        if row[type_column] != native_type:
            native = df.loc[
                (df["name"] == row["name"]) &
                (df["threads"] == row["threads"]) &
                (df["input"] == row["input"]) &
                (df["compiler"] == row["compiler"]) &
                (df[type_column] == native_type),
                native_column
            ]
            row["overhead"] = float(row[column] / native) if not native.empty else np.nan
            # check_overhead(row)
            df.iloc[i] = row  # copy the result into the dataframe

    return df


def calculate_ratio(df, columns, over):
    for column in columns:
        df[column] = df[column] / df[over]  # in python3 / returns float, no need to convert
    return df


def calculate_multithreading_overhead(df, column="time", over=2):
    df["overhead"] = np.nan
    for i, row in df.iterrows():
        if row["threads"] != over:
            native = df.loc[
                (df["name"] == row["name"]) &
                (df["type"] == row["type"]) &
                (df["compiler"] == row["compiler"]) &
                (df["compilertype"] == row["compilertype"]) &
                (df["input"] == row["input"]) &
                (df["threads"] == over),
                column
            ]
            row["overhead"] = float(native / row[column]) if not native.empty else np.nan
            #check_overhead(row)
            df.iloc[i] = row  # copy the result into the dataframe
    return df

# === Namings and orders ===
BUILD_NAMES = {
    "long": {
        "clang-native":         "Native (Clang)",
        "safecode-enabled":     "SAFECode (Clang)",
        "safecode-native":      "Native (SAFECode)",
        "clang-asan":           "ASan (Clang)",
        "clang-asan_no_quarantine":           "ASan nq (Clang)",
        "softbound-enabled":    "SoftBound (Clang)",
        "softbound-native":     "Native (SoftBound)",

        "icc-native":                          "Native (ICC)",
        "icc-mpx_no_narrow_bounds_only_write": "MPX n.n.b. o.w. (ICC)",
        "icc-mpx_no_narrow_bounds":            "MPX n.n.b. (ICC)",
        "icc-mpx_only_write":                  "MPX o.w. (ICC)",
        "icc-mpx":                             "MPX (ICC)",

        "gcc-native":                          "Native (GCC)",
        "gcc-mpx_no_narrow_bounds_only_write": "MPX n.n.b. o.w. (GCC)",
        "gcc-mpx_no_narrow_bounds":            "MPX n.n.b. (GCC)",
        "gcc-mpx_only_write":                  "MPX o.w. (GCC)",
        "gcc-mpx":                             "MPX (GCC)",
        "gcc-asan":                            "ASan (GCC)",
        "gcc-asan_only_write":                 "ASan o.w. (GCC)",
    },
    "short": {
        "clang-native":         "Native (Clang)",
        "safecode-enabled":     "SAFECode",
        "safecode-native":      "Native (SAFECode)",
        "clang-asan":           "ASan",
        "clang-asan_no_quarantine": "ASan nq (Clang)",
        "softbound-enabled":    "SoftBound",
        "softbound-native":     "Native (SoftBound)",

        "icc-native":                          "Native (ICC)",
        "icc-mpx_no_narrow_bounds_only_write": "MPX (ICC)",
        "icc-mpx_no_narrow_bounds":            "MPX (ICC)",
        "icc-mpx_only_write":                  "MPX (ICC)",
        "icc-mpx":                             "MPX (ICC)",

        "gcc-native":                          "Native (GCC)",
        "gcc-mpx_no_narrow_bounds_only_write": "MPX (GCC)",
        "gcc-mpx_no_narrow_bounds":            "MPX (GCC)",
        "gcc-mpx_only_write":                  "MPX (GCC)",
        "gcc-mpx":                             "MPX (GCC)",
        "gcc-asan":                            "ASan",
        "gcc-asan_only_write":                 "ASan",
    },
    "tiny": {
        "Native (Clang)": r"$N$",
        "SAFECode (Clang)": r"$C$",
        "ASan (Clang)": r"$A$",
        "SoftBound (Clang)": r"$B$",

        "Native (ICC)": r"$N$",
        "MPX n.n.b. (ICC)": r"$I$",
        "MPX o.w. (ICC)": r"$\bar{I}$",
        "MPX (ICC)": r"$I$",

        "Native (GCC)": r"$N$",
        "MPX n.n.b. (GCC)": r"$G$",
        "MPX o.w. (GCC)": r"$\bar{G}$",
        "MPX (GCC)": r"$G$",
        "ASan (GCC)": r"$A$",
    },
    "empty": {
        "clang-native": "",
        "safecode-enabled": "",
        "clang-asan": "",
        "softbound-enabled": "",

        "icc-native": "",
        "icc-mpx_no_narrow_bounds_only_write": "",
        "icc-mpx_no_narrow_bounds": "",
        "icc-mpx_only_write": "",
        "icc-mpx": "",

        "gcc-native": "",
        "gcc-mpx_no_narrow_bounds_only_write": "",
        "gcc-mpx_no_narrow_bounds": "",
        "gcc-mpx_only_write": "",
        "gcc-mpx": "",
        "gcc-asan": "",
        "gcc-asan_only_write": "",
    },
    "mpx_feature": {
        "icc-native": "Native (ICC)",
        "icc-mpx_no_narrow_bounds_only_write": "No narrow bounds only write (ICC)",
        "icc-mpx_no_narrow_bounds": "No narrow bounds (ICC)",
        "icc-mpx_only_write": "Only write (ICC)",
        "icc-mpx": "Full (ICC)",

        "gcc-native": "Native (GCC)",
        "gcc-mpx_no_narrow_bounds_only_write": "No narrow bounds only write (GCC)",
        "gcc-mpx_no_narrow_bounds": "No narrow bounds (GCC)",
        "gcc-mpx_only_write": "Only write (GCC)",
        "gcc-mpx": "Full (GCC)",
    }
}

INPUT_NAMES = {
    "long": {
        0: "Small",
        1: "Medium",
        2: "Large",
        3: "Extra Large",
        4: "XXL"
    },
    "short": {
        0: "S",
        1: "M",
        2: "L",
        3: "XL",
        4: "XXL"
    }
}

DEFAULT_BUILD_ORDER = (
    "clang-asan",
    "clang-asan_no_quarantine",
    "icc-mpx",
    "gcc-mpx",
    "safecode-enabled",
    "softbound-enabled",
)
OTHER_BUILD_ORDERS = {
    "mpxcount": (
        "icc-mpx",
        "icc-mpx_only_write",
        "gcc-mpx",
        "gcc-mpx_only_write",
    ),
    "multi": (
        "gcc-native",
        "clang-asan",
        "icc-mpx",
        "gcc-mpx",
    ),
    "native_mem_access": (
        "clang-native",
        "icc-native",
        "gcc-native",
        "safecode-native",
        "softbound-native",
    ),
    "ipc": (
        "gcc-native",
        "clang-asan",
        "icc-mpx",
        "gcc-mpx",
        "safecode-enabled",
        "softbound-enabled",
    ),
    "cache": (
        "gcc-native",
        "clang-asan",
        "icc-mpx",
        "gcc-mpx",
        "safecode-enabled",
        "softbound-enabled",
    ),
    "mpx_feature_perf": (
        "icc-mpx",
        "icc-mpx_no_narrow_bounds",
        "icc-mpx_only_write",
        "gcc-mpx",
        "gcc-mpx_no_narrow_bounds",
        "gcc-mpx_only_write",
    ),
    "mpx_feature_mem": (
        "icc-mpx",
        "icc-mpx_no_narrow_bounds",
        "icc-mpx_only_write",
        "gcc-mpx",
        "gcc-mpx_no_narrow_bounds",
        "gcc-mpx_only_write",
    ),
    "tput": (
        "gcc-native",
        "gcc-asan",
        "icc-mpx_no_narrow_bounds",
        "gcc-mpx_no_narrow_bounds",
    ),
}


def rename_build(df, long=True):
    columns = BUILD_NAMES["long"] if long else BUILD_NAMES["short"]
    df.rename(columns=columns, inplace=True)


def reorder_compilers(df, t):
    orders = defaultdict(list, **OTHER_BUILD_ORDERS)
    orders.default_factory = lambda: DEFAULT_BUILD_ORDER
    df["compilertype"] = Categorical(df["compilertype"], orders[t], ordered=True)
    df.sort_values(["compilertype"], inplace=True)


def reorder_and_rename_benchmarks(df, order):
    """
    Polymorphic function:
        if `order` is a list, only reorders benchmarks
        if it is an ordered dictionary, also renames
        other types are forbidden
    """
    if type(order) is tuple:
        df["name"] = Categorical(df["name"], order, ordered=True)
        df.sort_values(["name"], inplace=True)
    elif type(order) is OrderedDict:
        df["name"] = Categorical(df["name"], list(order.keys()), ordered=True)
        df.sort_values(["name"], inplace=True)
        df.name.cat.rename_categories(list(order.values()), inplace=True)
    else:
        logging.error("Wrong type of the benchmark list!")
        raise TypeError


# === Shortcuts ===
def list_diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]
