#!/usr/bin/env python3
"""
Merges several csv files (the first file serves as base)
Assumes that they have the same set of columns,
but the columns do not have to be in the same order
"""

import csv
import sys


def main():
    if len(sys.argv) < 3:
        print("Wrong number of arguments: specify at least two files to merge!")
        exit(1)

    # get header
    with open(sys.argv[1], "r") as merge_to:
        header = csv.DictReader(merge_to).fieldnames

    # copy
    with open(sys.argv[1], "a") as merge_to:
        writer = csv.DictWriter(merge_to, fieldnames=header)

        for i in range(2, len(sys.argv)):
            with open(sys.argv[i], "r") as merge_from:
                reader = csv.DictReader(merge_from)
                for row in reader:
                    # print(row)
                    writer.writerow(row)


if __name__ == '__main__':
    main()
