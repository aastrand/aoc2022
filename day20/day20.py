#!/usr/bin/env python3

import sys
from dataclasses import dataclass

from utils import io


@dataclass
class DoubleLinkedListNode:
    num: int
    next = None
    prev = None

    def insert_after(self, other):
        self.next = other
        self.prev = other.prev
        other.prev.next = self
        other.prev = self

    def remove(self):
        tmp = self.next
        self.next.prev = self.prev
        self.prev.next = tmp


def print_list(pc, size):
    for _ in range(0, size):
        print(pc.num, "", end="")
        pc = pc.next
    print()


def print_list_prev(pc, size):
    pc = pc.prev
    for _ in range(0, size):
        print(pc.num, "", end="")
        pc = pc.prev
    print()


def parse(lines, multiplier=1):
    nums = []
    head = None
    zero = None
    prev = None
    for line in lines:
        num = int(line) * multiplier
        next = DoubleLinkedListNode(num)
        nums.append(next)

        next.prev = prev
        if prev:
            prev.next = next

        if head is None:
            head = next

        if num == 0:
            zero = next

        prev = next

    next.next = head
    head.prev = next

    return nums, zero


def mix(nums):
    for _, cur in enumerate(nums):
        moving = cur

        if moving.num == 0:
            continue

        for _ in range(0, (moving.num) % (len(nums) - 1)+1):
            cur = cur.next

        moving.remove()
        moving.insert_after(cur)


def score(cur):
    sum = 0
    for i in range(0, 3001):
        if i % 1000 == 0:
            sum += cur.num
        cur = cur.next

    return sum


def part1(filename):
    nums, zero = parse(io.get_lines(filename))

    mix(nums)

    return score(zero)


def part2(filename):
    nums, zero = parse(io.get_lines(filename), 811589153)

    for _ in range(0, 10):
        mix(nums)

    return score(zero)


def main():
    assert part1("example.txt") == 3
    print(part1("../input/2022/day20.txt"))

    assert part2("example.txt") == 1623178306
    print(part2("../input/2022/day20.txt"))


if __name__ == "__main__":
    sys.exit(main())
