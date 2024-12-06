########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    nsafe=0
    for report in input_str.strip().split('\n'):
        plevel=None
        incr=None
        safe=True
        for level in report.split(' '):
            l=int(level)
            if plevel is None:
                plevel=l
                continue
            d=abs(l-plevel)
            if d<1 or d>3:
                safe=False
                break
            if incr is None:
                incr=(l>plevel)
                plevel=l
                continue
            if (l>plevel and not incr) or (l<plevel and incr):
                safe=False
                break
            else:
                plevel=l
        if safe:
            nsafe+=1
    return nsafe

def solve_2(input_str):
    nsafe=0
    for report in input_str.strip().split('\n'):
        if is_safe(report):
            nsafe+= 1
            continue
        rep=report.strip().split(' ')
        for i in range(len(report)):
            r=' '.join(rep[:i]+rep[i+1:])
            if is_safe(r):
                nsafe+=1
                break
    return nsafe

def parse_input(input_str):
    pass

def is_safe(report):
    plevel=None
    incr=None
    safe=True
    for level in report.split(' '):
        l=int(level)
        if plevel is None:
            plevel=l
            continue
        d=abs(l-plevel)
        if d<1 or d>3:
            safe=False
            break
        if incr is None:
            incr=(l>plevel)
            plevel=l
            continue
        if (l>plevel and not incr) or (l<plevel and incr):
            safe=False
            break
        else:
            plevel=l
    return safe

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""", 2),
                ]
        self.tc_2 = [
                (
"""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""", 4),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
