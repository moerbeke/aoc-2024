########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

input_parsed = False
before_rules = {}
after_rules = {}
updates = []

def solve_1(input_str):
    parse_input(input_str)
    s = 0
    for u in updates:
        violation = False
        for i in range(len(u)-1):
            p1 = u[i]
            if p1 in after_rules:
                for p2 in after_rules[p1]:
                    if p2 in u[i+1:]:
                        violation = True
                        break
            if violation:
                break
        if not violation:
            s += u[len(u)//2]
    return s

def solve_2(input_str):
    parse_input(input_str)
    s = 0
    for u in updates:
        violation = False
        for i in range(len(u)-1):
            p1 = u[i]
            if p1 in after_rules:
                for p2 in after_rules[p1]:
                    if p2 in u[i+1:]:
                        violation = True
                        break
            if violation:
                break
        if violation:
            s += correct_update(u)[len(u)//2]
    return s

def correct_update(u):
    if len(u) == 0:
        return []
    else:
        pindex = get_first_page_index(u)
        return [u[pindex]] + correct_update(u[:pindex]+u[pindex+1:])

def get_first_page_index(u):
    for i in range(len(u)):
        p1 = u[i]
        is_first = True
        for p2 in u[:i]+u[i+1:]:
            if p2 in before_rules and p1 in before_rules[p2]:
                is_first = False
                break
        if is_first:
            pindex = i
            break
    assert(is_first)
    return pindex

def parse_input(input_str):
    global input_parsed
    if input_parsed:
        return
    input_parsed = True
    rules_str, updates_str = input_str.strip().split('\n\n')
    for r in rules_str.strip().split('\n'):
        x, y = r.split('|')
        x = int(x)
        y = int(y)
        if x not in before_rules:
            before_rules[x] = [y]
        else:
            before_rules[x].append(y)
        if y not in after_rules:
            after_rules[y] = [x]
        else:
            after_rules[y].append(x)
    for u in updates_str.strip().split('\n'):
        updates.append([int(p) for p in u.split(',')])
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
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""", 143),
                ]
        self.tc_2 = [
                (
"""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""", 123),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
