"""
Preparation stage: how results are averaged and aggregated

TODO: this file is in urgent need of cleaning and refactoring
"""
import os
from collections import defaultdict, OrderedDict

from pandas import read_csv, DataFrame, Categorical, Series
import numpy as np
import logging

import config

conf = config.Config()


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
    columns = conf.aggregated_data

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
def rename_build(df, long=True):
    columns = conf.build_names["long"] if long else conf.build_names["short"]
    df.rename(columns=columns, inplace=True)


def reorder_compilers(df, t):
    orders = defaultdict(list, **conf.other_build_orders)
    orders.default_factory = lambda: conf.default_build_order
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
