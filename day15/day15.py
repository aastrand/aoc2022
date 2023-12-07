#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass

from utils import io
from utils.math import manhattan_dist

RE = re.compile(
    'Sensor at x=([-]?[0-9]+), y=([-]?[0-9]+): closest beacon is at x=([-]?[0-9]+), y=([-]?[0-9]+)')


@dataclass
class Sensor:
    pos: tuple
    minY: int
    maxY: int
    dist: int

    def intersect_y(self, y):
        pts = []
        if y >= self.minY and y <= self.maxY:
            dist = self.dist - abs(y - self.pos[1])
            pts.append(self.pos[0] - dist)
            pts.append(self.pos[0] + dist)

        return pts


def parse(lines):
    sensors = []

    for line in lines:
        m = RE.match(line)
        coords = [int(g) for g in m .groups()]
        dist = manhattan_dist(coords[0], coords[1], coords[2], coords[3])
        minY = coords[1] - dist
        maxY = coords[1] + dist - 1

        sensors.append(Sensor((coords[0], coords[1]), minY, maxY, dist))

    return sensors


def part1(filename, trace=10):
    sensors = parse(io.get_lines(filename))

    hits = set()
    for s in sensors:
        if trace >= s.minY and trace <= s.maxY:
            pts = s.intersect_y(trace)
            for x in range(pts[0], pts[1]):
                hits.add(x)

    return len(hits)


def merge(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    ret = []

    for i in intervals:
        new = i
        if ret:
            if ret[-1][1] >= i[0]-1:
                new = ret.pop()
                if i[1] > new[1]:
                    new[1] = i[1]
        ret.append(new)

    return ret


def part2(filename, max=20):
    sensors = parse(io.get_lines(filename))

    pos = None
    for y in range(0, max+1):
        intervals = []
        for s in sensors:
            if y >= s.minY and y <= s.maxY:
                intervals.append(s.intersect_y(y))

        merged = merge(intervals)
        if len(merged) > 1:
            pos = (merged[0][1]+1, y)
            break

    return (pos[0] * 4000000) + y


def main():
    assert part1("example.txt") == 26
    print(part1("../input/2022/day15.txt", 2000000))

    assert part2("example.txt") == 56000011
    print(part2("../input/2022/day15.txt", 4000000))


if __name__ == "__main__":
    sys.exit(main())
