#!/usr/bin/env python3

import sys

from utils import io

MAPPING = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}


REVERSE_MAPPING = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "="
}


SIZES = [
    -2,
    -1,
    0,
    1,
    2,
]


def from_snafu(num):
    sum = 0

    for i in range(len(num)-1, -1, -1):
        idx = len(num)-1-i
        sum += MAPPING[num[i]] * 5**idx

    return sum


def maxxed(e):
    sum = 0

    while e > 0:
        sum += (5**e)*2
        e -= 1

    return sum


def find_starter_bit(num):
    sum = 0
    exp = 1

    best_val = None
    best_exponent = None
    smallest_diff = float('inf')
    while sum < num and best_exponent is None:
        sum = 5 ** exp

        for val in SIZES:
            test = (sum * val) - num
            if test > 0 and test < smallest_diff:
                smallest_diff = test
                best_val = val
                best_exponent = exp

        exp += 1

    exp = best_exponent
    val = best_val

    sum = (5**exp)*val
    if maxxed(exp-1) < (sum - num):
        if val == 1:
            exp -= 1
            val = 2
        else:
            val -= 1

    return exp, val


def to_snafu(num):
    nums = []

    exp, val = find_starter_bit(num)

    sum = (5**exp)*val
    nums.append((exp, val))

    while exp > 0:
        exp -= 1

        smallest_diff = float('inf')
        for val in SIZES:
            test = (sum + ((5**exp)*val)) - num

            if abs(test) < smallest_diff:
                smallest_diff = abs(test)
                best_val = val

        nums.append((exp, best_val))
        sum += (5**exp)*best_val

    return ''.join([REVERSE_MAPPING[num[1]] for num in nums])


def part1(filename):
    lines = io.get_lines(filename)

    sum = 0
    for line in lines:
        sum += from_snafu(line)

    return to_snafu(sum)


def main():
    assert from_snafu("20") == 10
    assert from_snafu("2=") == 8
    assert from_snafu("1=0") == 15
    assert from_snafu("2=-01") == 976
    assert from_snafu("1=11-2") == 2022
    assert from_snafu("1-0---0") == 12345
    assert from_snafu("1121-1110-1=0") == 314159265

    assert to_snafu(10) == "20"
    assert to_snafu(15) == "1=0"
    assert to_snafu(20) == "1-0"
    assert to_snafu(2022) == "1=11-2"
    assert to_snafu(314159265) == "1121-1110-1=0"

    assert to_snafu(4890) == "2=-1=0"

    assert part1("example.txt") == "2=-1=0"
    print(part1("../input/2022/day25.txt"))


if __name__ == "__main__":
    sys.exit(main())
