########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

BOX = 'O'
WALL = '#'
EMPTY = '.'
ROBOT = '@'
LBOX = '['
RBOX = ']'

def solve_1(input_str):
    m, moves, robot, X, Y = parse_input(input_str)
    boxes = process_moves(m, moves, robot, X, Y)
    gps_coords = sum([100*y+x for (x,y) in boxes])
    return gps_coords

def solve_2(input_str):
    m, moves, robot, X, Y = parse_input(input_str)
    m, robot, X, Y = widen(m, X, Y)
    boxes = process_moves(m, moves, robot, X, Y, scale_up=True)
    gps_coords = sum([100*y+x for (x,y) in boxes])
    return gps_coords

def process_moves(m, moves, robot, X, Y, scale_up=False):
    boxes = []
    print_map(m, X, Y)
    for move in moves:
        m, robot = process_move(m, move, robot, X, Y, scale_up)
    for p in m:
        if m[p] == BOX or m[p] == LBOX:
            boxes.append(p)
    return boxes

def process_move(m, move, robot, X, Y, scale_up):
    rx, ry = robot
    dx, dy = {
            '^': (0, -1),
            'v': (0, +1),
            '<': (-1, 0),
            '>': (+1, 0)}[move]
    if scale_up:
        try_move = try_move_2
    else:
        try_move = try_move_1
    m, robot = try_move(m, dx, dy, robot, X, Y)
    print_map(m, X, Y)
    return m, robot

def try_move_1(m, dx, dy, robot, X, Y):
    rx, ry = robot
    empty = None
    x, y = robot
    while empty is None:
        if m[(x,y)] == WALL:
            break
        elif m[(x,y)] == EMPTY:
            empty = (x,y)
            break
        x += dx
        y += dy
    if empty is not None:
        ex, ey = empty
        n = abs(ex-rx) + abs(ey-ry)
        for i in range(n):
            (x,y) = (ex-i*dx,ey-i*dy)
            assert(m[(x,y)] != WALL)
            m[(x,y)] = m[(x-dx,y-dy)]
        m[(rx,ry)] = EMPTY
        robot = (rx+dx,ry+dy)
    return m, robot

def try_move_2(m, dx, dy, robot, X, Y):
    if dy == 0:
        return try_move_1(m, dx, dy, robot, X, Y)
    rx, ry = robot
    if m[(rx,ry+dy)] == WALL:
        return m, robot
    if m[(rx,ry+dy)] == EMPTY:
        m[(rx,ry+dy)] = ROBOT
        m[(rx,ry)] = EMPTY
        robot = (rx,ry+dy)
        return m, robot
    boxes = []
    if m[(rx,ry+dy)] == LBOX:
        can_move = can_push(m, dy, robot, rx, ry+dy, X, Y, boxes)
    elif m[(rx,ry+dy)] == RBOX:
        can_move = can_push(m, dy, robot, rx-1, ry+dy, X, Y, boxes)
    else:
        assert(False)
    if can_move:
        boxes = sorted(boxes, key=lambda b: b[1])
        if dy > 0:
            boxes = reversed(boxes)
        for bx,by in boxes:
            m[(bx,by+dy)] = LBOX
            m[(bx+1,by+dy)] = RBOX
            m[(bx,by)] = EMPTY
            m[(bx+1,by)] = EMPTY
        m[(rx,ry+dy)] = ROBOT
        m[(rx,ry)] = EMPTY
        robot = (rx,ry+dy)
    return m, robot

def can_push(m, dy, robot, bx, by, X, Y, boxes):
    boxes.append((bx,by))
    if m[(bx,by+dy)] == EMPTY and m[(bx+1,by+dy)] == EMPTY:
        return True
    elif m[(bx,by+dy)] == LBOX and m[(bx+1,by+dy)] == RBOX:
        return can_push(m, dy, robot, bx, by+dy, X, Y, boxes)
    elif m[(bx,by+dy)] == EMPTY and m[(bx+1,by+dy)] == LBOX:
        return can_push(m, dy, robot, bx+1, by+dy, X, Y, boxes)
    elif m[(bx,by+dy)] == RBOX and m[(bx+1,by+dy)] == EMPTY:
        return can_push(m, dy, robot, bx-1, by+dy, X, Y, boxes)
    elif m[(bx,by+dy)] == RBOX and m[(bx+1,by+dy)] == LBOX:
        return can_push(m, dy, robot, bx-1, by+dy, X, Y, boxes) and can_push(m, dy, robot, bx+1, by+dy, X, Y, boxes)
    else:
        assert(m[(bx,by+dy)] == WALL or m[(bx+1,by+dy)] == WALL)
        return False

def widen(m, X, Y):
    robot = None
    for y in range(Y):
        for x in range(X-1, -1, -1):
            if m[(x,y)] == WALL:
                m[(2*x,y)] = WALL
                m[(2*x+1,y)] = WALL
            elif m[(x,y)] == EMPTY:
                m[(2*x,y)] = EMPTY
                m[(2*x+1,y)] = EMPTY
            elif m[(x,y)] == BOX:
                m[(2*x,y)] = LBOX
                m[(2*x+1,y)] = RBOX
            elif m[(x,y)] == ROBOT:
                m[(2*x,y)] = ROBOT
                m[(2*x+1,y)] = EMPTY
                robot = 2*x, y
    X *= 2
    return m, robot, X, Y

def print_map(m, X, Y):
    printable = ""
    for y in range(Y):
        for x in range(X):
            printable += m[(x,y)]
        printable += "\n"
    verboseprint(printable)

def parse_input(input_str):
    m = {}
    moves = ''
    robot = (-1,-1)
    m_str, moves_str = input_str.strip().split('\n\n')
    y = 0
    for line in m_str.split('\n'):
        x = 0
        for c in line:
            m[(x,y)] = c
            if c == ROBOT:
                robot = (x,y)
            x += 1
        X = x
        y += 1
    Y = y
    moves = ''.join(moves_str.strip().split('\n'))
    return m, moves, robot, X, Y

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""", 2028),
                (
"""
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""", 10092),
                ]
        self.tc_2 = [
                (
"""
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""", 9021),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
