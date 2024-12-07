########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from itertools import product as combr

ADD = '+'
MULTIPLY = '*'
CONCAT = '||'
OPERATORS = [ADD, MULTIPLY]
EXT_OPERATORS = [ADD, MULTIPLY, CONCAT]

def solve_1(input_str):
    values, eqs = parse_input(input_str)
    s = 0
    for i in range(len(values)):
        value = values[i]
        eq = eqs[i]
        if is_feasible(value, eq):
            s += value
    return s

def solve_2(input_str):
    values, eqs = parse_input(input_str)
    s = 0
    for i in range(len(values)):
        value = values[i]
        eq = eqs[i]
        if is_feasible(value, eq, True):
            s += value
    return s

def is_feasible(value, eq, extended=False):
    feasible = False
    n_operators = len(eq) - 1
    if extended:
        combs = combr(EXT_OPERATORS, repeat=n_operators)
    else:
        combs = combr(OPERATORS, repeat=n_operators)
    verboseprint(value, eq, "?")
    for operators in combs:
        teq = eq.copy()
        for op in operators:
            if op == MULTIPLY:
                result = teq[0] * teq[1]
            elif op == ADD:
                result = teq[0] + teq[1]
            elif op == CONCAT:
                assert(extended)
                result = teq[0] * 10**len(str(teq[1])) + teq[1]
            else:
                assert(False)
            if result > value:
                break
            teq = [result] + teq[2:]
        if len(teq) > 1:
            continue
        s = teq[0]
        if s == value:
            feasible = True
            verboseprint("Feasible", operators)
            break
    return feasible

def parse_input(input_str):
    values = []
    eqs = []
    for line in input_str.strip().split('\n'):
        value, operands = line.split(':')
        value = int(value.strip())
        operands = [int(o.strip()) for o in operands.strip().split(' ')]
        values.append(value)
        eqs.append(operands)
    return values, eqs

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""", 3749),
                ]
        self.tc_2 = [
                (
"""
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""", 11387),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
