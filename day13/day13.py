#!/usr/bin/env python3

import functools
import json
import sys

from utils import io


def compare(left, right):
    # print("comparing", left, "vs", right)

    # If both values are integers, the lower integer should come first.
    if type(left) == int and type(right) == int:
        # If the left integer is lower than the right integer, the inputs are in the right order.
        # If the left integer is higher than the right integer, the inputs are not in the right order.
        if left < right:
            return -1
        if left > right:
            return 1

        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        return 0

    # If both values are lists, compare the first value of each list, then the second value, and so on.
    if type(left) == list and type(right) == list:
        for i in range(0, min(len(left), len(right))):
            cmp = compare(left[i], right[i])
            if cmp != 0:
                return cmp

        # If the left list runs out of items first, the inputs are in the right order.
        if len(left) < len(right):
            return -1

        # If the right list runs out of items first, the inputs are not in the right order.
        if len(left) > len(right):
            return 1

        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        return 0

    # If exactly one value is an integer, convert the integer to a list
    # which contains that integer as its only value, then retry the comparison.
    # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2);
    # the result is then found by instead comparing [0,0,0] and [2].
    if type(left) == int:
        left = [left]
    elif type(right) == int:
        right = [right]

    return compare(left, right)


def part1(filename):
    lines = io.get_input(filename).split("\n\n")

    sum = 0
    for i, pair in enumerate(lines):
        parts = pair.split("\n")
        left = json.loads(parts[0])
        right = json.loads(parts[1])

        # print("# comparing idx", i + 1, left, "vs", right)
        if compare(left, right) == -1:
            # print("# => idx", i + 1, "right order")
            sum += i + 1
        # else:
        #    print("# => idx", i + 1, "NOT IN right order")

    return sum


def part2(filename):
    lines = io.get_input(filename).split("\n\n")

    packets = []
    d1 = [[2]]
    d2 = [[6]]
    packets.append(d1)
    packets.append(d2)

    for pair in lines:
        parts = pair.split("\n")
        packets.append(json.loads(parts[0]))
        packets.append(json.loads(parts[1]))

    packets.sort(key=functools.cmp_to_key(compare))

    product = 1
    for i, p in enumerate(packets):
        if p == d1 or p == d2:
            product *= i+1

    return product


def main():
    assert compare([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) == -1
    assert compare([0, 0, 0], 2) == -1

    assert part1("example.txt") == 13
    print(part1("../input/2022/day13.txt"))

    assert part2("example.txt") == 140
    print(part2("../input/2022/day13.txt"))


if __name__ == "__main__":
    sys.exit(main())
