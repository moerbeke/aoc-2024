#!/usr/bin/env python3

########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

import argparse
import importlib
import unittest

########################################################################
# Generic input parser and solver invoker for daily puzzle
########################################################################

def aoc():
    global daysolver
    global verboseprint
    year = 2022
    args = parse_cmd_line_args()
    print("\n===== AoC-%d day #%d =====\n" % (year, args.day))
    day = str(args.day)
    if args.day < 10:
        day =  '0' + day
    daysolver = importlib.import_module('aoc' + day)
    if args.verbose:
        daysolver.verboseprint = print
    else:
        daysolver.verboseprint = lambda *a, **k : None
    if args.test:
        print("======== Unit tests =======")
        run_test(day, daysolver)
    else:
        input_filename = day + '.in'
        input_str = read_file(input_filename)
        if args.part_2_only:
            output_1 = None
        else:
            output_1 = daysolver.solve_1(input_str)
            print("Answer 1:", output_1)
        if args.part_1_only:
            output_2 = None
        else:
            output_2 = daysolver.solve_2(input_str)
            print("Answer 2:", output_2)
        return output_1, output_2

def parse_cmd_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int, choices=range(1, 25+1), help="Advent day (1-25)", metavar='day')
    parser.add_argument("-v", "--verbose", help="print verbose output", action="store_true")
    part_group = parser.add_mutually_exclusive_group()
    part_group.add_argument("-t", "--test", help="run unit tests", action="store_true")
    part_group.add_argument("-p1", "--part-1-only", help="solve part 1 only", action="store_true")
    part_group.add_argument("-p2", "--part-2-only", help="solve part 2 only", action="store_true")
    args = parser.parse_args()
    return args

def read_file(filename):
    """Read a file and return its contents as a multiline string.
    """
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

def suite(TestClass):
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestClass))
    return test_suite

def run_test(day, daysolver):
    aoc_test_suite = unittest.TestSuite()
    aoc_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(daysolver.TestAoc))
    runner = unittest.TextTestRunner()
    runner.run(aoc_test_suite)

if __name__ == '__main__':
    aoc()
