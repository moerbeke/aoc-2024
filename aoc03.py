########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import re

def solve_1(input_str):
    mem = ''.join(parse_input(input_str).split('\n'))
    return do_mul(mem)

def solve_2(input_str):
    mem = ''.join(parse_input(input_str).split('\n'))
    s = 0
    while mem is not None:
        do_dont = mem.split("don't()", maxsplit=1)
        do_mem = do_dont[0]
        s += do_mul(do_mem)
        if len(do_dont) == 1:
            mem = None
        else:
            assert(len(do_dont) ==2)
            dont_mem = do_dont[1]
            dont_do = dont_mem.split("do()", maxsplit=1)
            if len(dont_do) == 1:
                mem = None
            else:
                assert(len(dont_do) ==2)
                mem = dont_do[1]
    return s

def do_mul(mem):
    s = 0
    for mul in re.findall(r'mul\([0-9]+,[0-9]+\)', mem):
        a, b = [int(n) for n in re.findall(r'[0-9]+', mul)]
        s += a*b
    return s

def parse_input(input_str):
    return input_str.strip()

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""", 161),
                ]
        self.tc_2 = [
                (
"""
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""", 48),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
