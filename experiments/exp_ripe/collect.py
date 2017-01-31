#!/usr/bin/env python
from __future__ import absolute_import

from core import collect


def main():
    # set parameters
    full_output_file = collect.data + "/ripe/ripe.log"
    results_file = collect.data + "/ripe/raw.csv"
    parameters = {
        "ok":          ["TOTAL OK:", lambda l: collect.get_int_from_string(l)],
        "some":        ["TOTAL SOME:", lambda l: collect.get_int_from_string(l)],
        "fail":        ["TOTAL FAIL:", lambda l: collect.get_int_from_string(l)],
        "notpossible": ["TOTAL NP:", lambda l: collect.get_int_from_string(l)],
        "total":       ["TOTAL ATTACKS:", lambda l: collect.get_int_from_string(l)],
    }
    # collect
    collect.collect(results_file, full_output_file, parameters)
