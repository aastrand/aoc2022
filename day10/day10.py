#!/usr/bin/env python3

import sys

from utils import io


class CPU:
    def __init__(self, mem):
        self.X = 1
        self.mem = mem
        self.ip = 0
        self.cur = None
        self.work = 0

    def cycle(self):
        if self.cur is None:
            self.cur = self.mem[self.ip]
            self.ip += 1

            if self.cur[0] == "noop":
                self.work = 1
            else:
                self.work = 2

        self.work -= 1

        if self.work == 0:
            if self.cur[0] == "addx":
                self.addx(int(self.cur[1]))

            self.cur = None

    def addx(self, v):
        self.X += v


def part1(filename):
    mem = [line.split(" ") for line in io.get_lines(filename)]
    cpu = CPU(mem)
    samples = set([20, 60, 100, 140, 180, 220])

    sum = 0
    for i in range(1, max(samples)+1):
        if i in samples:
            sum += cpu.X * i
        cpu.cycle()

    return sum


def part2(filename):
    mem = [line.split(" ") for line in io.get_lines(filename)]
    cpu = CPU(mem)

    for _ in range(0, 6):
        row = []
        for c in range(0, 40):
            if c >= cpu.X - 1 and c <= cpu.X + 1:
                row.append("#")
            else:
                row.append(".")
            cpu.cycle()

        print(''.join(row))


def main():
    assert part1("example.txt") == 13140
    print(part1("input.txt"))

    part2("example.txt")
    part2("input.txt")


if __name__ == "__main__":
    sys.exit(main())
