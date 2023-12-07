#!/usr/bin/env python3

import sys
from collections import deque

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP

MOVES = [
    LEFT,
    BOTTOM,
    RIGHT,
    TOP,
    (0, 0),
]

OBS = {
    "^": 0,
    "v": 1,
    ">": 2,
    "<": 3
}


def in_bounds(bounds, pos):
    return pos[0] >= bounds[0] and pos[0] < bounds[1] \
        and pos[1] >= bounds[2] and pos[1] < bounds[3]


def collision(obstacles, bounds, pos, time):
    up = (pos[0], (pos[1] + time) % bounds[3])
    down = (pos[0], (pos[1] - time) % bounds[3])
    right = ((pos[0] - time) % bounds[1], pos[1])
    left = ((pos[0] + time) % bounds[1], pos[1])

    return up in obstacles[0] or \
        down in obstacles[1] or \
        right in obstacles[2] or \
        left in obstacles[3]


def walk(start, goal, bounds, obstacles, time=0):
    q = deque()

    while len(q) == 0:
        time += 1
        if not collision(obstacles, bounds, start, time):
            q.append((start, time))

    visited = set()
    while True:
        pos, time = q.popleft()

        key = (pos, time)
        if key in visited:
            continue

        visited.add(key)

        # make decisions
        for o in MOVES:
            new_pos = (pos[0] + o[0], pos[1] + o[1])

            # in goal
            if new_pos == goal:
                return time + 1

            if new_pos == start or \
                (in_bounds(bounds, new_pos) and
                 not collision(obstacles, bounds, new_pos, time+1)):
                q.append((new_pos, time+1))


def find_obstacles(lines):
    obstacles = [
        set(),
        set(),
        set(),
        set(),
    ]
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            if val != ".":
                obstacles[OBS[val]].add((x, y))

    return obstacles


def parse(lines):
    lines = [line[1:-1] for line in lines[1:-1]]

    s = (0, 0)
    e = (len(lines[0])-1, len(lines))

    obstacles = find_obstacles(lines)

    return (0, len(lines[0]),
            0, len(lines)), obstacles, s, e


def part1(filename):
    bounds, obstacles, s, e = parse(io.get_lines(filename))

    return walk(s, e, bounds, obstacles)


def part2(filename):
    bounds, obstacles, s, e = parse(io.get_lines(filename))

    steps = walk(s, e, bounds, obstacles)
    steps = walk(e, s, bounds, obstacles, steps)
    steps = walk(s, e, bounds, obstacles, steps)

    return steps


def main():
    bounds, obstacles, s, e = parse(io.get_lines("move_example.txt"))
    assert s == (0, 0)
    assert e == (4, 5)
    assert bounds == (0, 5, 0, 5)

    assert in_bounds((1, 5, 1, 5), (2, 5)) is False
    assert in_bounds((1, 5, 1, 5), (0, 4)) is False
    assert in_bounds((1, 5, 1, 5), (1, 4)) is True
    assert in_bounds((1, 5, 1, 5), (0, 0)) is False
    assert in_bounds((1, 5, 1, 5), (6, 6)) is False
    assert in_bounds((1, 5, 1, 5), (-1, -1)) is False

    assert not collision(obstacles, bounds, (0, 0), 0)
    assert collision(obstacles, bounds, (0, 1), 0)  # >
    assert collision(obstacles, bounds, (0, 2), 0)  # <
    assert collision(obstacles, bounds, (2, 3), 0)  # ^
    assert collision(obstacles, bounds, (3, 3), 0)  # v

    assert not collision(obstacles, bounds, (0, 0), 1)
    assert collision(obstacles, bounds, (1, 1), 1)  # >
    assert collision(obstacles, bounds, (4, 2), 1)  # <
    assert collision(obstacles, bounds, (2, 2), 1)  # ^
    assert collision(obstacles, bounds, (3, 4), 1)  # v

    assert not collision(obstacles, bounds, (0, 0), 2)
    assert collision(obstacles, bounds, (2, 1), 2)  # >
    assert collision(obstacles, bounds, (3, 2), 2)  # <
    assert collision(obstacles, bounds, (2, 1), 2)  # ^
    assert collision(obstacles, bounds, (3, 0), 2)  # v

    assert not collision(obstacles, bounds, (0, 0), 3)
    assert collision(obstacles, bounds, (3, 1), 3)  # >
    assert collision(obstacles, bounds, (2, 2), 3)  # <
    assert collision(obstacles, bounds, (2, 0), 3)  # ^
    assert collision(obstacles, bounds, (3, 1), 3)  # v

    assert not collision(obstacles, bounds, (0, 0), 4)
    assert collision(obstacles, bounds, (4, 1), 4)  # >
    assert collision(obstacles, bounds, (1, 2), 4)  # <
    assert collision(obstacles, bounds, (2, 4), 4)  # ^
    assert collision(obstacles, bounds, (3, 2), 4)  # v

    assert not collision(obstacles, bounds, (0, 0), 5)
    assert collision(obstacles, bounds, (0, 1), 5)  # >
    assert collision(obstacles, bounds, (0, 2), 5)  # <
    assert collision(obstacles, bounds, (2, 3), 5)  # ^
    assert collision(obstacles, bounds, (3, 3), 5)  # v

    bounds, obstacles, s, e = parse(io.get_lines("example.txt"))
    assert bounds == (0, 6, 0, 4)
    assert not collision(obstacles, bounds, (5, 0), 1)
    assert not collision(obstacles, bounds, (5, 0), 2)
    assert not collision(obstacles, bounds, (5, 0), 3)
    assert collision(obstacles, bounds, (5, 0), 4)
    assert collision(obstacles, bounds, (5, 0), 5)
    assert collision(obstacles, bounds, (5, 0), 6)
    assert not collision(obstacles, bounds, (5, 0), 7)
    assert not collision(obstacles, bounds, (5, 0), 8)
    assert not collision(obstacles, bounds, (5, 0), 9)
    assert collision(obstacles, bounds, (5, 0), 10)
    assert collision(obstacles, bounds, (5, 0), 11)
    assert collision(obstacles, bounds, (5, 0), 12)

    assert part1("example.txt") == 18
    print(part1("../input/2022/day24.txt"))

    assert part2("example.txt") == 54
    print(part2("../input/2022/day24.txt"))


if __name__ == "__main__":
    sys.exit(main())
