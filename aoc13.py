########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

"""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

94n + 22m = 8400
34n + 67m = 5400
"""

def solve_1(input_str):
    machines = parse_input(input_str)
    return compute_tokens(machines)

def solve_2(input_str):
    machines = parse_input(input_str)
    return compute_tokens(machines, high=True)

def compute_tokens(machines, high=False):
    """
    ax*m + bx*n = px
    ay*m + by*n = py
    m = (bx*py - by*px)/(ay*bx - ax*by)
    n = (ax*py - ay*px)/(ax*by - ay*bx)
    """
    if high:
        h = 10000000000000
    n_tokens = 0
    for (ax, ay, bx, by, px, py) in machines:
        if high:
            px += h
            py += h
        m = (bx*py - by*px)//(ay*bx - ax*by)
        n = (ax*py - ay*px)//(ax*by - ay*bx)
        if m >= 0 and n >= 0 and ax*m + bx*n == px and ay*m + by*n == py:
            n_tokens += 3*m + n
    return n_tokens

def parse_input(input_str):
    machines = []
    for machine in input_str.strip().split('\n\n'):
        a, b, p = machine.split('\n')
        ax = int(a[a.index('+')+1:a.index(',')])
        ay = int(a[a.rindex('+')+1:])
        bx = int(b[b.index('+')+1:b.index(',')])
        by = int(b[b.rindex('+')+1:])
        px = int(p[p.index('=')+1:p.index(',')])
        py = int(p[p.rindex('=')+1:])
        machines.append((ax,ay, bx,by, px,py))
    return machines

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""", 480),
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
