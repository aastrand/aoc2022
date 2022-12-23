#!/usr/bin/env python3

import copy
import sys

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP, Grid

# import time


R = 0
D = 1
L = 2
U = 3


MOVEMENTS = [
    RIGHT,
    BOTTOM,
    LEFT,
    TOP
]

FACING = [
    ">",
    "v",
    "<",
    "^"
]


def find_start(grid, pos=[0, 0], offset=(1, 0)):
    pos = list(pos)

    while grid.get((pos)) == " " or grid.get((pos)) is None:
        pos[0] += offset[0]
        pos[1] += offset[1]

    return pos


def next_pos(grid, pos, facing):
    offset = MOVEMENTS[facing]
    new_pos = [pos[0] + offset[0], pos[1] + offset[1]]

    val = grid.get(new_pos)
    if val == ".":
        return new_pos

    if val == " " or val is None:
        if facing == 0:
            new_pos = find_start(grid, [0, pos[1]], offset)
        elif facing == 1:
            new_pos = find_start(grid, [pos[0], 0], offset)
        elif facing == 2:
            new_pos = find_start(grid, [grid.maxX, pos[1]], offset)
        elif facing == 3:
            new_pos = find_start(grid, [pos[0], grid.maxY+1], offset)

    if grid.get(new_pos) == ".":
        return new_pos

    return pos


def parse(input):
    parts = input.split("\n\n")
    grid = Grid.from_lines(parts[0].split("\n"))

    instructions = []
    cur = []
    for c in parts[1].strip():
        if c == "R" or c == "L":
            instructions.append((int("".join(cur)), c))
            cur = []
        else:
            cur.append(c)

    instructions.append((int("".join(cur)), ''))

    return grid, instructions


def part1(filename):
    grid, instructions = parse(io.get_input(filename))

    pos = find_start(grid)
    facing = 0

    # print_grid = copy.deepcopy(grid)
    for instr in instructions:
        # print_grid.set((pos), FACING[facing])
        for _ in range(0, instr[0]):
            pos = next_pos(grid, pos, facing)
            # print_grid.set((pos), FACING[facing])

        if instr[1] == "R":
            facing += 1
        elif instr[1] == "L":
            facing -= 1
        facing = facing % 4

    return ((pos[1] + 1) * 1000) + (4 * (pos[0] + 1)) + facing


#         1111
#         1111
#         1111
#         1111
# 222233334444
# 222233334444
# 222233334444
# 222233334444
#         55556666
#         55556666
#         55556666
#         55556666

EXAMPLE_BOUNDS = {
    1: ((8, 0), (11, 3)),
    2: ((0, 4), (3, 7)),
    3: ((4, 4), (7, 7)),
    4: ((8, 4), (11, 7)),
    5: ((8, 8), (11, 11)),
    6: ((12, 8), (15, 11))
}

EXAMPLE_CUBE = {
    (1, U): (2, D),
    (1, D): (4, D),
    (1, L): (3, D),
    (1, R): (6, L),

    (2, U): (1, D),
    (2, D): (5, U),
    (2, L): (6, U),
    (2, R): (3, R),

    (3, U): (1, R),
    (3, D): (5, R),
    (3, L): (2, L),
    (3, R): (4, R),

    (4, U): (1, U),
    (4, D): (5, D),
    (4, L): (3, L),
    (4, R): (6, D),

    (5, U): (4, U),
    (5, D): (2, U),
    (5, L): (3, U),
    (5, R): (6, R),

    (6, U): (4, L),
    (6, D): (2, R),
    (6, L): (5, L),
    (6, R): (1, L),
}

BOUNDS = {
    1: ((50, 0), (99, 49)),
    2: ((100, 0), (149, 49)),
    3: ((50, 50), (99, 99)),
    4: ((0, 100), (49, 149)),
    5: ((50, 100), (99, 149)),
    6: ((0, 150), (49, 199)),
}

CUBE = {
    (1, U): (6, R),
    (1, D): (3, D),
    (1, L): (4, R),
    (1, R): (2, R),

    (2, U): (6, U),
    (2, D): (3, L),
    (2, L): (1, L),
    (2, R): (5, L),

    (3, U): (1, U),
    (3, D): (5, D),
    (3, L): (4, D),
    (3, R): (2, U),

    (4, U): (3, R),
    (4, D): (6, D),
    (4, L): (1, R),
    (4, R): (5, R),

    (5, U): (3, U),
    (5, D): (6, L),
    (5, L): (4, L),
    (5, R): (2, L),

    (6, U): (4, U),
    (6, D): (2, D),
    (6, L): (1, D),
    (6, R): (5, U),
}


def in_quadrant(pos, bounds):
    for quad, coords in bounds.items():
        if pos[0] >= coords[0][0] and pos[0] <= coords[1][0] and \
                pos[1] >= coords[0][1] and pos[1] <= coords[1][1]:
            return quad

    return None


def next_pos_cube(grid, pos, facing, cube, bounds):
    q = in_quadrant(pos, bounds)

    offset = MOVEMENTS[facing]
    new_pos = [pos[0] + offset[0], pos[1] + offset[1]]

    new_q = in_quadrant(new_pos, bounds)

    val = grid.get(new_pos)

    # all was fine
    if val == "." and new_q is not None:
        return new_pos, facing

    if new_q is None:
        new_q, new_facing = cube[(q, facing)]

        old_bounds = bounds[q]
        new_bounds = bounds[new_q]

        rel_pos = (pos[0] - old_bounds[0][0], pos[1] - old_bounds[0][1])

        size = old_bounds[1][0] - old_bounds[0][0]  # 49 for input

        # transform pos
        if (facing, new_facing) == (U, U):
            new_rel_pos = (rel_pos[0], size)
        elif (facing, new_facing) == (U, L):
            new_rel_pos = (size, rel_pos[0])
        elif (facing, new_facing) == (U, R):
            new_rel_pos = (0, rel_pos[0])
        elif (facing, new_facing) == (U, D):
            new_rel_pos = (0, size - rel_pos[1])

        elif (facing, new_facing) == (D, D):
            new_rel_pos = (rel_pos[0], 0)
        elif (facing, new_facing) == (D, L):
            new_rel_pos = (size, rel_pos[0])
        elif (facing, new_facing) == (D, R):
            new_rel_pos = (0, size - rel_pos[1])
        elif (facing, new_facing) == (D, U):
            new_rel_pos = (size - rel_pos[0], size)

        elif (facing, new_facing) == (L, L):
            new_rel_pos = (size, rel_pos[1])
        elif (facing, new_facing) == (L, R):
            new_rel_pos = (0, size-rel_pos[1])
        elif (facing, new_facing) == (L, D):
            new_rel_pos = (rel_pos[1], 0)
        elif (facing, new_facing) == (L, U):
            new_rel_pos = (size, size-rel_pos[0])

        elif (facing, new_facing) == (R, R):
            new_rel_pos = (0, rel_pos[1])
        elif (facing, new_facing) == (R, L):
            new_rel_pos = (size, size-rel_pos[1])
        elif (facing, new_facing) == (R, D):
            new_rel_pos = (size - rel_pos[1], 0)
        elif (facing, new_facing) == (R, U):
            new_rel_pos = (rel_pos[1], size)

        # transform back
        new_pos = (new_rel_pos[0] + new_bounds[0][0],
                   new_rel_pos[1] + new_bounds[0][1])

        # check if val == "."
        # if so return
        new_val = grid.get(new_pos)
        if new_val is None:
            print("something went wrong", pos, facing)
            quit()
        if new_val == ".":
            return new_pos, new_facing

    # ran into something, stay in place
    return pos, facing


def part2(filename, cube, bounds):
    grid, instructions = parse(io.get_input(filename))

    pos = find_start(grid)
    facing = 0

    print_grid = copy.deepcopy(grid)
    for instr in instructions:
        for _ in range(0, instr[0]):
            pos, facing = next_pos_cube(grid, pos, facing, cube, bounds)
            print_grid.set(pos, FACING[facing])

        if instr[1] == "R":
            facing += 1
        elif instr[1] == "L":
            facing -= 1
        facing = facing % 4

    return ((pos[1] + 1) * 1000) + (4 * (pos[0] + 1)) + facing


def main():
    assert part1("example.txt") == 6032
    print(part1("input.txt"))

    assert in_quadrant((8, 0), EXAMPLE_BOUNDS) == 1

    assert part2("example.txt", EXAMPLE_CUBE, EXAMPLE_BOUNDS) == 5031
    print(part2("input.txt", CUBE, BOUNDS))


if __name__ == "__main__":
    sys.exit(main())
