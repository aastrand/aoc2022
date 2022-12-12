#!/usr/bin/env python3

import sys

from utils import io
from utils.graph import dijkstra, from_grid, get_path
from utils.grid import Grid


def elevation(a, b):
    if a == 'S':
        a = 'a'
    elif b == 'S':
        b = 'a'

    if a == 'E':
        a = 'z'
    elif b == 'E':
        b = 'z'

    return ord(b) - ord(a)


def parse(lines):
    grid = Grid.from_lines(lines)
    s = None
    e = None

    for pos, val in grid.data.items():
        if val == "S":
            s = pos
        elif val == "E":
            e = pos

    return s, e, grid


def part1(filename):
    s, e, grid = parse(io.get_lines(filename))
    graph = from_grid(grid, lambda _p, _n, val,
                      other: elevation(val, other) <= 1)

    path, _, _ = dijkstra(graph, s, e)

    return len(path) - 1


def part2(filename):
    s, e, grid = parse(io.get_lines(filename))
    graph = from_grid(grid, lambda _p, _n, val,
                      other: elevation(val, other) >= -1)

    path, _, prev = dijkstra(graph, e, s)

    min = len(path) - 1
    for pos, val in grid.data.items():
        if val == 'a':
            path = get_path(prev, e, pos)
            if (len(path) - 1) < min and len(path) > 1:
                min = len(path) - 1

    return min


def main():
    assert part1("example.txt") == 31
    print(part1("input.txt"))

    assert part2("example.txt") == 29
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
