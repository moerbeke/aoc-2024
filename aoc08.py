########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    m, am, X, Y = parse_input(input_str)
    n = compute_antinodes(m, am, X, Y)
    return n

def solve_2(input_str):
    m, am, X, Y = parse_input(input_str)
    n = compute_resonant_antinodes(m, am, X, Y)
    return n

def compute_antinodes(m, am, X, Y):
    antinodes = set()
    for f in am:
        for i in range(len(am[f])):
            x1, y1 = am[f][i]
            peers = am[f][:i]
            if i+1 < len(am[f]):
                peers += am[f][i+1:]
            for (x2,y2) in peers:
                dx = x2 - x1
                dy = y2 - y1
                a = x2 + dx
                b = y2 + dy
                if in_map(a, b, X, Y):
                    antinodes.add((a,b))
                a = x1 - dx
                b = y1 - dy
                if in_map(a, b, X, Y):
                    antinodes.add((a,b))
    return len(antinodes)

def compute_resonant_antinodes(m, am, X, Y):
    antinodes = set()
    for f in am:
        for i in range(len(am[f])):
            x1, y1 = am[f][i]
            peers = am[f][:i]
            if i+1 < len(am[f]):
                peers += am[f][i+1:]
            for (x2,y2) in peers:
                antinodes.add((x2,y2))
                dx = x2 - x1
                dy = y2 - y1
                for k in range(1, X):
                    kdx = k * dx
                    kdy = k * dy
                    a = x2 + kdx
                    b = y2 + kdy
                    if in_map(a, b, X, Y):
                        antinodes.add((a,b))
                    else:
                        break
                for k in range(1, X):
                    kdx = k * dx
                    kdy = k * dy
                    a = x1 - kdx
                    b = y1 - kdy
                    if in_map(a, b, X, Y):
                        antinodes.add((a,b))
                    else:
                        break
    return len(antinodes)

def in_map(x, y, X, Y):
    return 0<=x<X and 0<=y<Y

def parse_input(input_str):
    X = -1
    Y = -1
    m = {}
    am = {}
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            m[(x,y)] = c
            if '0'<=c<='9' or 'A'<=c<='Z' or 'a'<=c<='z':
                if c not in am:
                    am[c] = [(x,y)] 
                else:
                    am[c].append((x,y))
            x += 1
        X = x
        y += 1
    Y = y
    return m, am, X, Y

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
""", 2),
                (
"""
..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
""", 4),
                (
"""
..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
""", 4),
                (
"""
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""", 14),
                ]
        self.tc_2 = [
                (
"""
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
""", 9),
                (
"""
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
""", 34),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
