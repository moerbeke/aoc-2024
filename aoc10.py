########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from math import inf

HEAD = 0
PEAK = 9

X = -1
Y = -1
m = None
heads = None

rating = None

def solve_1(input_str):
    parse_input(input_str)
    return compute_trail_heads()

def solve_2(input_str):
    parse_input(input_str)
    compute_trail_heads()
    return rating

def compute_trail_heads():
    global rating
    rating = 0
    head_peaks = {}
    for head in heads:
        head_peaks[head] = compute_peaks(head)
    score = 0
    for head in head_peaks:
        score += len(head_peaks[head])
    return score

def compute_peaks(head):
    tm = {}
    tm[head] = HEAD
    expand(head, tm)
    peaks = []
    for p in tm:
        if tm[p] == PEAK:
            peaks.append(p)
    return peaks

def expand(p0 ,tm):
    h0 = tm[p0]
    x0, y0 = p0
    for p in [(x0-1,y0), (x0+1,y0), (x0,y0-1), (x0,y0+1)]:
        x, y = p
        if 0<=x<X and 0<=y<Y and m[p] == h0 + 1:
            tm[p] = h0 + 1
            if h0 + 1 == PEAK:
                global rating
                rating += 1
            else:
                expand(p, tm)

def parse_input(input_str):
    global X, Y, m, heads
    m = {}
    heads = []
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            try:
                h = int(c)
            except ValueError:        
                h = inf
            m[(x,y)] = h
            if h == HEAD:
                heads.append((x,y))
            x += 1
        X = x
        y += 1
    Y = y
    return

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
0123
1234
8765
9876
""", 1),
                (
"""
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
""", 2),
                (
"""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
""", 4),
                (
"""
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
""", 3),
                (
"""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""", 36),
                ]
        self.tc_2 = [
                (
"""
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
""", 3),
                (
"""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
""", 13),
                (
"""
012345
123456
234567
345678
4.6789
56789.
""", 227),
                (
"""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""", 81),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
