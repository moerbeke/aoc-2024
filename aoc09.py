########################################################################
# Advent of Code 2024 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

SPACE = '.'

def solve_1(input_str):
    disk_map = parse_input(input_str)
    compacted_disk = compact(disk_map)
    return compute_checksum(compacted_disk)

def solve_2(input_str):
    disk_map = parse_input(input_str)
    compacted_disk = compact_no_fragments(disk_map)
    return compute_checksum(compacted_disk)

def compact(disk_map):
    disk = []
    is_file = True
    file_id = 0
    for n in disk_map:
        size = int(n)
        if is_file:
            disk += [str(file_id)] * size
            file_id += 1
        else:
            disk += [SPACE] * size
        is_file = not is_file
    space_ptr = disk.index(SPACE)
    data_ptr = len(disk) - 1
    while data_ptr > space_ptr:
        if disk[data_ptr] != SPACE:
            disk[space_ptr] = disk[data_ptr]
            disk[data_ptr] = SPACE
            space_ptr += disk[space_ptr:].index(SPACE)
        data_ptr -= 1
    for d in disk[disk.index(SPACE):]:
        assert(d == SPACE)
    return disk

def compact_no_fragments(disk_map):
    disk = []
    is_file = True
    file_id = 0
    ptr = 0
    spaces = {}
    files = {}
    for n in disk_map:
        size = int(n)
        if is_file:
            disk += [str(file_id)] * size
            files[ptr] = (file_id, size)
            file_id += 1
        elif size > 0:
            disk += [SPACE] * size
            spaces[ptr] = size
        is_file = not is_file
        ptr += size
    assert(ptr == len(disk))
    verboseprint("".join(disk))
    for file_ptr in reversed(files.keys()):
        file_id, file_size = files[file_ptr]
        for space_ptr in sorted(spaces.keys()):
            if space_ptr + file_size > file_ptr:
                break
            if spaces[space_ptr] >= file_size:
                for i in range(file_size):
                    disk[space_ptr+i] = str(file_id)
                    disk[file_ptr+i] = SPACE
                if spaces[space_ptr] > file_size:
                    spaces[space_ptr+file_size] = spaces[space_ptr] - file_size
                del spaces[space_ptr]
                verboseprint("".join(disk))
                break
    return disk

def compute_checksum(disk):
    checksum = 0
    n = 0
    for data in disk:
        if data != SPACE:
            checksum += n*int(data)
        n += 1
    return checksum

def parse_input(input_str):
    return input_str.strip()

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
2333133121414131402
""", 1928),
                ]
        self.tc_2 = [
                (
"""
2333133121414131402
""", 2858),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        self.assertEqual(''.join(compact(parse_input('12345'))), '022111222......')
        self.assertEqual(''.join(compact(parse_input('2333133121414131402'))), '0099811188827773336446555566..............')
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
