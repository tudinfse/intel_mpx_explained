#!/usr/bin/env python
from __future__ import absolute_import

from core import collect


def main():
    full_output_file = collect.data + "/micro_perf/micro_perf.log"
    results_file = collect.data + "/micro_perf/raw.csv"
    collect.collect(results_file, full_output_file)
