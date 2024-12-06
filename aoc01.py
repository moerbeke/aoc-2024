########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    x, y = parse_input(input_str)
    d = sum([abs(x[i]-y[i]) for i in range(len(x))])
    return d

def solve_2(input_str):
    x, y = parse_input(input_str)
    s = 0
    for a in x:
        c = 0
        for b in y:
            if b == a:
                c += 1
        s += a*c
    return s

def parse_input(input_str):
    x = []
    y = []
    for line in input_str.strip().split('\n'):
        a,b = line.split('  ')
        x.append(int(a))
        y.append(int(b))
    x = sorted(x)
    y = sorted(y)
    return x, y

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
3   4
4   3
2   5
1   3
3   9
3   3
""", 11),
                ]
        self.tc_2 = [
                (
"""
3   4
4   3
2   5
1   3
3   9
3   3
""", 31),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
