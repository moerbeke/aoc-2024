########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

GUARD = '^'
BLOCK = '#'
EMPTY = '.'
PATH = 'X'
U = 'U'
D = 'D'
R = 'R'
L = 'L'
dirs = [U, R, D, L]
X = None
Y = None

def solve_1(input_str):
    gx, gy, gd, m = parse_input(input_str)
    n = 0
    inside = True
    while inside:
        verboseprint(gx,gy,gd)
        if 0<=gx<X and 0<=gy<Y:
            if m[(gx,gy)] == EMPTY:
                m[(gx,gy)] = PATH
                n += 1
            assert(m[(gx,gy)] == PATH)
            gx, gy, gd, m = move(gx, gy, gd, m)
        else:
            inside = False
    return n

def solve_2(input_str):
    solve_1(input_str)
    gx, gy, gd, m = parse_input(input_str)
    n = 0
    for y in range(X):
        for x in range(Y):
            if m[(x,y)] == BLOCK or (x,y) == (gx,gy):
                continue
            verboseprint(x,y)
            if is_loop(gx, gy, gd, x, y, m):
                verboseprint("Loop")
                n += 1
    return n

def move(gx, gy, gd, m):
    dx, dy = {
            U: (0,-1),
            R: (1,0),
            D: (0,1),
            L: (-1,0)
            }[gd]
    ngx = gx + dx
    ngy = gy + dy
    if ngx < 0 or ngx >= X or ngy < 0 or ngy >= Y or m[(gx+dx,gy+dy)] != BLOCK:
        gx = ngx
        gy = ngy
    else:
        gd = dirs[(dirs.index(gd)+1)%4]
    return gx, gy, gd, m

def is_loop(gx, gy, gd, x, y, m):
    tm = m.copy()
    tm[(x,y)] = BLOCK
    inside = True
    path = []
    while inside:
        if (gx,gy,gd) in path:
            return True
        path.append((gx,gy,gd))
        if 0<=gx<X and 0<=gy<Y:
            if tm[(gx,gy)] == EMPTY:
                tm[(gx,gy)] = PATH
            assert(tm[(gx,gy)] == PATH)
            gx, gy, gd, m = move(gx, gy, gd, tm)
        else:
            inside = False
    return False

def parse_input(input_str):
    global X, Y
    m = {}
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for p in line:
            if p == GUARD:
                gx,gy = x,y
                gd = U
                m[(x,y)] = EMPTY
            elif p == EMPTY:
                m[(x,y)] = EMPTY
            elif p == BLOCK:
                m[(x,y)] = BLOCK
            else:
                assert(False)
            x += 1
        X = x
        y += 1
    Y = y
    return gx, gy, gd, m

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""", 41),
                ]
        self.tc_2 = [
                (
"""
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""", 6),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
