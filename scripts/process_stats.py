#!/usr/bin/env python3
"""
Reads stats file and prints the following data:
- lines with number of runs != 10; TODO: num. runs as an argument
- variance higher than 5%
- ??

TODO: all these parameters as CLI arguments
"""

import csv
import sys


def report_row(row, reason):
    print(reason + ": " +
          row["--name"] + "," +
          row["--compiler"] + "," +
          row["--type"] + "," +
          row["--threads"] + "," +
          row["--input"])


def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments: specify one and only one file to process!")
        exit(1)

    t = "multi"
    correct_num_runs = 10
    variance_limit = 5.0

    columns_to_process = {
        "perf": (
            "cycles",
            "time",
            "instructions"
        ),
        "cache": (
            "time",
            "instructions"
        ),
        "mem": (
            "maxsize",
            "time",

        ),
        "multi": (
            "time",
        ),
    }

    # create a usable statistics table
    stat_table = []
    with open(sys.argv[1], "r") as original_file:
        reader = csv.reader(original_file)

        # combine three first line into a single header
        line1 = reader.__next__()
        line2 = reader.__next__()
        line3 = reader.__next__()
        header = ''
        for i, _ in enumerate(line1):
            header += line1[i] + '-' + line2[i] + '-' + line3[i] + ','

        # remove dangling comma and finish the header with new line
        stat_table.append(header[:-1])

        # copy the rest of the file as is
        for row in reader:
            stat_table.append(",".join(row))

    # prepare column names to ches
    num_runs_columns = [i + "-count_nonzero-" for i in columns_to_process[t]]
    variance_columns = [i + "-cvpct-" for i in columns_to_process[t]]

    reader = csv.DictReader(stat_table)
    for row in reader:
        # check variance
        for column in variance_columns:
            if row[column] and float(row[column]) > variance_limit:
                report_row(row, "High variance of " + column[:-1])
                break

        # check number of runs
        for column in num_runs_columns:
            if row[column] and float(row[column]) != correct_num_runs:
                report_row(row, "Wrong number of runs in " + column[:-1])
                break


if __name__ == '__main__':
    main()
