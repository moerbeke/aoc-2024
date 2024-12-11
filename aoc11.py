########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    arrangement = parse_input(input_str)
    for i in range(25):
        arrangement = blink(arrangement)
        if i < 5:
            verboseprint(sorted([int(i) for i in arrangement]))
    return len(arrangement)

def solve_2(input_str):
    arrangement = parse_input(input_str)
    p = pack(arrangement)
    for i in range(75):
        verboseprint(sorted([int(i) for i in p.keys()]))
        stones = p.keys()
        multipliers = p.copy()
        p = {}
        for stone in stones:
            pp = {}
            a = apply_rules(stone)
            for s in a:
                try:
                    pp[s] += 1
                except KeyError:
                    pp[s] = 1
            for s in pp:
                pp[s] *= multipliers[stone]
                try:
                    p[s] += pp[s]
                except KeyError:
                    p[s] = pp[s]
    return sum(p.values())

def blink(a):
    b = []
    for stone in a:
        output = apply_rules(stone)
        b += output
    return b

def pack(a):
    p = {}
    for stone in a:
        try:
            p[stone] += 1
        except KeyError:
            p[stone] = 1
    return p

def apply_rules(stone):
    output = []
    if stone == '0':
        output.append('1')
    elif len(stone) % 2 == 0:
        l = len(stone)
        for substone in [stone[:l//2], stone[l//2:]]:
            output.append(str(int(substone)))
    else:
        output.append(str(int(stone) * 2024))
    return output

def parse_input(input_str):
    return [n for n in input_str.strip().split(' ')]

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
125 17
""", 55312),
                ]
        self.tc_2 = [
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
