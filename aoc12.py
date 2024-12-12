########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

m = None
X = None
Y = None

def solve_1(input_str):
    parse_input(input_str)
    return compute_price()

def solve_2(input_str):
    parse_input(input_str)
    return compute_price(with_discount=True)

def compute_price(with_discount=False):
    if with_discount:
        compute_factor = count_sides
    else:
        compute_factor = compute_perimeter
    price = 0
    explored_region = []
    for y in range(Y):
        for x in range(X):
            if (x,y) in explored_region:
                continue
            region = []
            scan(x, y, m[(x,y)], region)
            area = len(region)
            factor = compute_factor(region)
            price += area * factor
            explored_region += region
    return price

def scan(x0, y0, plant, region):
    if 0<=x0<X and 0<=y0<Y and m[(x0,y0)] == plant:
        region += [(x0,y0)]
        for (x,y) in [(x0,y0-1), (x0-1,y0), (x0+1,y0), (x0, y0+1)]:
            if (x,y) in region:
                continue
            scan(x, y, plant, region)

def compute_perimeter(region):
    p = 0
    plant = m[region[0]]
    for (x0,y0) in region:
        for (x,y) in [(x0,y0-1), (x0-1,y0), (x0+1,y0), (x0, y0+1)]:
            if (not (0<=x<X and 0<=y<Y)) or m[(x,y)] != plant:
                p += 1
    return p

def count_sides(region):
    n_sides = 0
    plant = m[region[0]]
    xs = sorted([x for (x,y) in region])
    ys = sorted([y for (x,y) in region])
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    # Left sides
    r = region.copy()
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            if (x,y) not in r:
                continue
            r.remove((x,y))
            if x == 0 or m[(x-1,y)] != plant:
                y2 = y
                for yy in range(y+1, ymax+1):
                    if (x,yy) in r and (x == 0 or m[(x-1,yy)] != plant):
                        y2 = yy
                        r.remove((x,yy))
                    else:
                        break
                n_sides += 1
    # Right sides
    r = region.copy()
    for x in range(xmax, xmin-1,-1):
        for y in range(ymin, ymax+1):
            if (x,y) not in r:
                continue
            r.remove((x,y))
            if x == X-1 or m[(x+1,y)] != plant:
                for yy in range(y+1, ymax+1):
                    if (x,yy) in r and (x == X-1 or m[(x+1,yy)] != plant):
                        r.remove((x,yy))
                    else:
                        break
                n_sides += 1
    # Up sides
    r = region.copy()
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            if (x,y) not in r:
                continue
            r.remove((x,y))
            if y == 0 or m[(x,y-1)] != plant:
                for xx in range(x+1, xmax+1):
                    if (xx,y) in r and (y == 0 or m[(xx,y-1)] != plant):
                        r.remove((xx,y))
                    else:
                        break
                n_sides += 1
    # Down sides
    r = region.copy()
    for y in range(ymax, ymin-1, -1):
        for x in range(xmin, xmax+1):
            if (x,y) not in r:
                continue
            r.remove((x,y))
            if y == Y-1 or m[(x,y+1)] != plant:
                for xx in range(x+1, xmax+1):
                    if (xx,y) in r and (y == Y-1 or m[(xx,y+1)] != plant):
                        r.remove((xx,y))
                    else:
                        break
                n_sides += 1
    return n_sides

def parse_input(input_str):
    global m, X, Y
    m = {}
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for plant in line:
            m[(x,y)] = plant
            x += 1
        X = x
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
AAAA
BBCD
BBCC
EEEC
""", 140),
                (
"""
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""", 772),
                (
"""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""", 1930),
                ]
        self.tc_2 = [
                (
"""
AAAA
BBCD
BBCC
EEEC
""", 80),
                (
"""
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""", 436),
                (
"""
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""", 236),
                (
"""
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""", 368),
                (
"""
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""", 1206),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
