#!/usr/bin/env python3

from utils import io
from utils import grid
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


MOVES = {
    'U': grid.TOP,
    'D': grid.BOTTOM,
    'L': grid.LEFT,
    'R': grid.RIGHT,
}


def sign(a): return (a > 0) - (a < 0)


def move_tail(t, h, offset, part2=False):
    diff = [abs(t[0] - h[0]), abs(t[1] - h[1])]

    # if touches, do nothing
    if abs(h[0] - t[0]) <= 1 and abs(h[1] - t[1]) <= 1:
        return t

    # if same row or col, move in same dir
    if t[0] == h[0]:
        t[1] = h[1] - sign(h[1] - t[1])
        return t
    elif t[1] == h[1]:
        t[0] = h[0] - sign(h[0] - t[0])
        return t

    # part 2, now the knot we are following can move diagonally
    if part2 and (abs(diff[0]) > 1 or abs(diff[1]) > 1):
        if abs(diff[0]) == 1:
            t[0] = h[0]
            t[1] = h[1] - sign(h[1] - t[1])
        elif abs(diff[1]) == 1:
            t[0] = h[0] - sign(h[0] - t[0])
            t[1] = h[1]
        else:
            t[0] = h[0] - sign(h[0] - t[0])
            t[1] = h[1] - sign(h[1] - t[1])
        return t

    # if diag, move same dir then align
    if abs(diff[0]) == 1:
        t[0] += h[0] - t[0]
        t[1] += offset[1]
        return t
    elif abs(diff[1]) == 1:
        t[0] += offset[0]
        t[1] += h[1] - t[1]
        return t

    print("shold not end up here", h, t, offset)
    quit()


def part1(filename):
    lines = io.get_lines(filename)

    h = [0, 0]
    t = [0, 0]

    visited = set()
    visited.add(tuple(t))

    for move in lines:
        parts = move.split(" ")
        dir = parts[0]
        steps = int(parts[1])

        offset = MOVES[dir]
        for s in range(0, steps):
            h[0] += offset[0]
            h[1] += offset[1]
            t = move_tail(t, h, offset)
            visited.add(tuple(t))

    return len(visited)


def part2(filename):
    lines = io.get_lines(filename)

    knots = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
             [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    visited = set()
    visited.add(tuple(knots[9]))

    for move in lines:
        parts = move.split(" ")
        dir = parts[0]
        steps = int(parts[1])

        offset = MOVES[dir]
        maxX = knots[0][0] + 5
        minX = knots[0][0] - 5
        maxY = knots[0][1] + 5
        minY = knots[0][1] - 5
        for s in range(0, steps):
            knots[0][0] += offset[0]
            knots[0][1] += offset[1]

            grid = {}
            grid[tuple(knots[0])] = 'H'
            maxX = max(maxX, knots[0][0])
            minX = min(minX, knots[0][0])
            maxY = max(maxY, knots[0][1])
            minY = min(minY, knots[0][1])

            for k in range(1, len(knots)):
                knots[k] = move_tail(knots[k], knots[k-1], offset, True)
                if tuple(knots[k]) not in grid:
                    grid[tuple(knots[k])] = k
                maxX = max(maxX, knots[k][0])
                minX = min(minX, knots[k][0])
                maxY = max(maxY, knots[k][1])
                minY = min(minY, knots[k][1])
            # print("move", dir, steps)
            # for y in range(minY, maxY+1):
            #     r = []
            #     for x in range(minX, maxX+1):
            #         r.append(str(grid.get((x, y), '.')))
            #     print("".join(r))
            # print()


            visited.add(tuple(knots[9]))

    # grid = {}
    # maxX = 0
    # minX = 0
    # maxY = 0
    # minY = 0
    # for v in visited:
    #     maxX = max(maxX, v[0])
    #     minX = min(minX, v[0])
    #     maxY = max(maxY, v[1])
    #     minY = min(minY, v[1])
    #     grid[v] = '#'
    # print()
    # for y in range(minY, maxY+1):
    #     r = []
    #     for x in range(minX, maxX+1):
    #         r.append(str(grid.get((x, y), '.')))
    #     print("".join(r))
    # print()

    return len(visited)


def main():
    assert part1("example.txt") == 13
    print(part1("input.txt"))

    # ......
    # ......
    # ......
    # ....H.
    # 4321..  (4 covers 5, 6, 7, 8, 9, s)

    # ......
    # ......
    # ....H.
    # .4321.
    # 5.....  (5 covers 6, 7, 8, 9, s)

    assert move_tail([2, 0], [4, -1], (0, -1), True) == [3, -1]
    assert move_tail([0, 0], [2, -2], (0, -1), True) == [1, -1]

    assert part2("example.txt") == 1
    assert part2("example2.txt") == 36
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
