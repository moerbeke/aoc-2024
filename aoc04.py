########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

X = None
Y = None
m = None
n_xmas = None

def solve_1(input_str):
    verboseprint("Part 1")
    global X
    global Y
    global m
    global n_xmas
    X = 0
    Y = 0
    m = {}
    n_xmas = 0
    parse_input(input_str)
    for y in range(Y):
        for x in range(X):
            scan(x,y)
    return n_xmas

def solve_2(input_str):
    verboseprint("Part 2")
    global X
    global Y
    global m
    global n_xmas
    X = 0
    Y = 0
    m = {}
    n_xmas = 0
    parse_input(input_str)
    for y in range(1,Y-1):
        for x in range(1,X-1):
            scan2(x,y)
    return n_xmas

def scan(x, y):
    global n_xmas
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            if is_xmas(x, y, dx, dy):
                n_xmas += 1

def scan2(x, y):
    global n_xmas
    for (dx,dy) in [(-1,-1), (1,1)]:
        if is_x_mas(x, y, dx, dy):
            n_xmas += 1

def is_xmas(x0, y0, dx, dy):
    match = True
    XMAS = 'XMAS'
    n = 0
    for c in XMAS:
        x = x0 + dx * n
        y = y0 + dy * n
        match = match and 0<=x<X and 0<=y<Y and m[(x,y)] == c
        if not match:
            break
        n += 1
    if match:
        verboseprint(x0,y0,dx,dy)
    return match

def is_x_mas(x0, y0, dx, dy):
    global px
    global py
    match = False
    if m[(x0,y0)] == 'A':
        n = 0
        dx1 = dx
        dy1 = dy
        dx2, dy2 = {
                (-1,-1): (-1,1),
                (1,1): (-1,1)
                }[(dx1,dy1)]
        if 0<=x0-1 and x0+1<X and 0<=y0-1 and y0+1<Y and (
                m[(x0+dx1,y0+dy1)] == 'M' and m[(x0-dx1,y0-dy1)] == 'S' and (
                    (m[(x0+dx2,y0+dy2)] == 'M' and m[(x0-dx2,y0-dy2)] == 'S') or (m[(x0+dx2,y0+dy2)] == 'S' and m[(x0-dx2,y0-dy2)] == 'M'))):
            match = True
    if match:
        verboseprint(x0,y0,dx,dy)
    return match

def parse_input(input_str):
    global X
    global Y
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            m[(x,y)] = c
            x += 1
        X = x
        x = 0
        y += 1
    Y = y

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
..X...
.SAMX.
.A..A.
XMAS.S
.X....
""", 4),
                (
"""
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
""", 18),
                (
"""
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""", 18),
                ]
        self.tc_2 = [
                (
"""
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
""", 9),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
