########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str, X=101, Y=103):
    robots = parse_input(input_str, X, Y)
    print_lobby(robots, X, Y)
    for i in range(100):
        for robot in robots:
            robot.move()
        print_lobby(robots, X, Y)
    return compute_safety_factor(robots, X, Y)

def solve_2(input_str, X=101, Y=103):
    robots = parse_input(input_str, X, Y)
    print_lobby(robots, X, Y)
    n = 0
    #is_tree = is_tree_by_uniqueness
    is_tree = is_tree_by_row
    while True:
        n += 1
        for robot in robots:
            robot.move()
        lobby = comp_lobby(robots, X, Y)
        verboseprint(n)
        if is_tree(lobby, X, Y):
            print_lobby(robots, X, Y)
            break
    return n

def compute_safety_factor(robots, X, Y):
    q1 = q2 = q3 = q4 = 0
    for robot in robots:
        x, y = robot.p
        if x < X//2:
            if y < Y//2:
                q1 += 1
            elif y > Y//2:
                q2 += 1
        elif x > X//2:
            if y < Y//2:
                q3 += 1
            elif y > Y//2:
                q4 += 1
    return q1 * q2 * q3 * q4

def comp_lobby(robots, X, Y):
    lobby = {}
    for robot in robots:
        p = robot.p
        try:
            lobby[p] += 1
        except KeyError:
            lobby[p] = 1
    return lobby

def is_tree_by_uniqueness(lobby, X, Y):
    for p in lobby:
        if lobby[p] != 1:
            return False
    return True

def is_tree_by_row(lobby, X, Y):
    for y in range(Y):
        n = 0
        lastx = -2
        for x in range(X):
            p = (x,y)
            if p in lobby and x == lastx+1:
                n += 1
                if n > 10:
                    return True
            else:
                n = 0
            lastx = x
    return False

def print_lobby(robots, X, Y):
    lobby = {}
    for y in range(Y):
        for x in range(X):
            lobby[(x,y)] = "."
    for robot in robots:
        p = robot.p
        if lobby[p] == ".":
            lobby[p] = "1"
        else:
            lobby[p] = str(int(lobby[p])+1%10)
    printable = ""
    for y in range(Y):
        for x in range(X):
            printable += lobby[(x,y)]
        printable += "\n"
    verboseprint(printable)

class Robot:

    def __init__(self, px, py, vx, vy, X, Y):
        self._px = px
        self._py = py
        self._vx = vx
        self._vy = vy
        self._X = X
        self._Y = Y

    @property
    def p(self):
        return (self._px,self._py)

    def move(self):
        self._px = (self._px + self._vx) % self._X
        self._py = (self._py + self._vy) % self._Y

def parse_input(input_str, X, Y):
    robots = []
    for line in input_str.strip().split('\n'):
        p, v = line.split(' ')
        px, py = [int(pi) for pi in p[p.index('=')+1:].split(',')]
        vx, vy = [int(vi) for vi in v[v.index('=')+1:].split(',')]
        robots.append(Robot(px, py, vx, vy, X, Y))
    return robots

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""", 12),
                ]
        self.tc_2 = [
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0], 11, 7), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
