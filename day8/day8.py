#!/usr/bin/env python3

from utils import io
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def is_visible(x, y, rows, cols):
    height = len(rows)
    width = len(cols)

    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
        return True

    val = int(rows[y][x])

    left = list(filter(lambda x: int(x) >= val, rows[y][:x]))
    right = list(filter(lambda x: int(x) >= val, rows[y][x+1:]))
    top = list(filter(lambda x: int(x) >= val, cols[x][:y]))
    bottom = list(filter(lambda x: int(x) >= val, cols[x][y+1:]))

    return len(left) == 0 or len(right) == 0 or len(top) == 0 or len(bottom) == 0


def parse(lines):
    rows = [list(r) for r in lines]
    height = len(rows)
    width = len(rows[0])
    cols = []
    for c in range(0, height):
        row = []
        for r in range(0, width):
            row.append(rows[r][c])
        cols.append(row)

    return rows, cols


def part1(filename):
    rows, cols = parse(io.get_lines(filename))
    height = len(rows)
    width = len(cols)

    sum = 0
    for c in range(0, width):
        for r in range(0, height):
            if is_visible(c, r, rows, cols):
                sum += 1

    return sum


def num_visible(val, trees):
    sum = 0
    for i in range(0, len(trees)):
        sum += 1
        if int(trees[i]) >= val:
            break

    return sum


def scenic_score(x, y, rows, cols):
    left = rows[y][:x]
    left.reverse()
    right = rows[y][x+1:]
    top = cols[x][:y]
    top.reverse()
    bottom = cols[x][y+1:]

    val = int(rows[y][x])

    return num_visible(val, left) * num_visible(val, right) * num_visible(val, top) * num_visible(val, bottom)


def part2(filename):
    rows, cols = parse(io.get_lines(filename))
    height = len(rows)
    width = len(cols)

    max = 0
    for c in range(0, width):
        for r in range(0, height):
            score = scenic_score(c, r, rows, cols)
            if score > max:
                max = score

    return max


def main():
    rows = [['3', '0', '3', '7', '3'], ['2', '5', '5', '1', '2'], [
        '6', '5', '3', '3', '2'], ['3', '3', '5', '4', '9'], ['3', '5', '3', '9', '0']]
    cols = [['3', '2', '6', '3', '3'], ['0', '5', '5', '3', '5'], [
        '3', '5', '3', '5', '3'], ['7', '1', '3', '4', '9'], ['3', '2', '2', '9', '0']]
    assert is_visible(1, 1, rows, cols) == True
    assert is_visible(2, 1, rows, cols) == True
    assert is_visible(3, 1, rows, cols) == False
    assert is_visible(1, 2, rows, cols) == True
    assert is_visible(2, 2, rows, cols) == False
    assert is_visible(3, 2, rows, cols) == True

    assert is_visible(1, 3, rows, cols) == False
    assert is_visible(2, 3, rows, cols) == True
    assert is_visible(3, 3, rows, cols) == False

    assert part1("example.txt") == 21
    print(part1("input.txt"))

    assert scenic_score(2, 1, rows, cols) == 4
    assert scenic_score(2, 3, rows, cols) == 8

    assert part2("example.txt") == 8
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
