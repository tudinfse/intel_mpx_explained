#!/usr/bin/env python
from __future__ import absolute_import

from core import collect


def main():
    collect.collect("ripe", user_parameters={
        "ok":          ["TOTAL OK:", lambda l: collect.get_int_from_string(l)],
        "some":        ["TOTAL SOME:", lambda l: collect.get_int_from_string(l)],
        "fail":        ["TOTAL FAIL:", lambda l: collect.get_int_from_string(l)],
        "notpossible": ["TOTAL NP:", lambda l: collect.get_int_from_string(l)],
        "total":       ["TOTAL ATTACKS:", lambda l: collect.get_int_from_string(l)],
    })
