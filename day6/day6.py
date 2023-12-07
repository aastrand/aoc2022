#!/usr/bin/env python3

import sys

from utils import io


def find_seq_index(s, length):
    for i in range(0, len(s) - length):
        if len(set(s[i:i+length])) == length:
            return i + length

    return None


def part1(filename):
    return find_seq_index(io.get_input(filename).strip(), 4)


def part2(filename):
    return find_seq_index(io.get_input(filename).strip(), 14)


def main():
    assert find_seq_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
    assert find_seq_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_seq_index("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_seq_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_seq_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

    print(part1("../input/2022/day6.txt"))

    assert find_seq_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert find_seq_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_seq_index("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_seq_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_seq_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

    print(part2("../input/2022/day6.txt"))


if __name__ == "__main__":
    sys.exit(main())
