#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import flood_fill_3d, neighbours_3d


def parse(lines):
    return set([tuple([int(c) for c in line.split(",")])
                for line in lines])


def exposed_surfaces(cubes):
    total = 6 * len(cubes)
    for c in cubes:
        for n in neighbours_3d(c):
            if n in cubes:
                total -= 1

    return total


def part1(filename):
    cubes = parse(io.get_lines(filename))

    return exposed_surfaces(cubes)


def part2(filename):
    cubes = parse(io.get_lines(filename))

    # walk bounding box that covers all cubes
    maxes, mins = [0, 0, 0], [float('inf'), float('inf'), float('inf')]
    for c in cubes:
        for i in range(0, 3):
            maxes[i] = max(maxes[i], c[i])
            mins[i] = min(mins[i], c[i])

    # make inverse set
    inverse = set()
    for x in range(mins[0]-1, maxes[0] + 1):
        for y in range(mins[1]-1, maxes[1] + 1):
            for z in range(mins[2]-1, maxes[2] + 1):
                cube = (x, y, z)
                if cube not in cubes:
                    inverse.add(cube)

    # out of inverse, which cubes are not connected with outmost corner position
    start = (maxes[0], maxes[1], maxes[1])
    visited = flood_fill_3d(start, cubes, (maxes, mins))
    for i in inverse:
        if i not in visited:
            cubes.add(i)

    # do surface calc on updated set, holes will be filled in now
    return exposed_surfaces(cubes)


def main():
    assert part1("example.txt") == 64
    print(part1("input.txt"))

    assert part2("example.txt") == 58
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
