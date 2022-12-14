#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import Grid


def get_from_grid(grid, x, y, floor):
    if floor is not None and y == floor:
        return '#'

    return grid.get((x, y))


def add_sand(grid, x, y, floor=None):
    if get_from_grid(grid, x, y, floor) is not None:
        return False

    while y <= max(floor if floor is not None else 0, grid.maxY):
        # v = grid.get((x, y))
        v = get_from_grid(grid, x, y, floor)
        if v is not None:
            # check left
            v = get_from_grid(grid, x-1, y, floor)
            if v is not None:
                # check right
                v = get_from_grid(grid, x+1, y, floor)
                if v is not None:
                    # stop where we fell
                    grid.set((x, y-1), 'o')
                    return True
                else:
                    # move right since it was open
                    x += 1
            else:
                # move left since it was open
                x -= 1
        else:
            # move down since it was open
            y += 1

    # fell outside
    return False


def parse(lines):
    grid = Grid()
    for line in lines:
        points = line.split(" -> ")
        for i in range(0, len(points)-1):
            p1 = [int(i) for i in points[i].split(',')]
            p2 = [int(i) for i in points[i+1].split(',')]

            if p1[0] == p2[0]:
                yf = min(p1[1], p2[1])
                yt = max(p1[1], p2[1])
                for y in range(yf, yt+1):
                    grid.set_at(p1[0], y, '#')
            else:
                xf = min(p1[0], p2[0])
                xt = max(p1[0], p2[0])
                for x in range(xf, xt+1):
                    grid.set_at(x, p1[1], '#')

    return grid


def part1(filename):
    grid = parse(io.get_lines(filename))

    sum = 0
    while add_sand(grid, 500, 0):
        sum += 1

    # grid.print_from(492, 503, 0, 12)

    return sum


def part2(filename):
    grid = parse(io.get_lines(filename))

    sum = 0
    floor = grid.maxY+2
    while add_sand(grid, 500, 0, floor):
        sum += 1

    # grid.print_from(492, 510, 0, 12)

    return sum


def main():
    assert part1("example.txt") == 24
    print(part1("input.txt"))

    assert part2("example.txt") == 93
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
