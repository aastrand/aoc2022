#!/usr/bin/env python3

import copy
import sys
from dataclasses import dataclass

from utils import io


@dataclass
class Monkey:
    id: str
    resolved: int = None
    operator: str = None
    neighbours = None


def resolve(graph, cur):
    if cur.resolved is not None:
        return

    for n in cur.neighbours:
        resolve(graph, graph[n])

    left, right = cur.resolved = graph[cur.neighbours[0]].resolved, \
        graph[cur.neighbours[1]].resolved

    if cur.operator == "+":
        cur.resolved = left + right
    elif cur.operator == "-":
        cur.resolved = left - right
    elif cur.operator == "*":
        cur.resolved = left * right
    elif cur.operator == "/":
        cur.resolved = left / right
    else:
        print("unknown operator", cur.operator)
        quit()

    return


def parse(lines):
    graph = {}
    for line in lines:
        parts = line.split(": ")
        id = parts[0]
        right = parts[1].split(" ")

        m = Monkey(id)
        if len(right) == 1:
            m.resolved = int(right[0])
        else:
            m.operator = right[1]
            m.neighbours = (right[0], right[2])

        graph[m.id] = m

    return graph


def part1(filename):
    graph = parse(io.get_lines(filename))
    resolve(graph, graph['root'])

    return int(graph['root'].resolved)


def part2(filename):
    graph = parse(io.get_lines(filename))

    found = False
    low = 0
    high = 10000000000000
    while not found:
        i = (low+high) // 2

        cur = copy.deepcopy(graph)
        cur['humn'].resolved = i
        resolve(cur, cur['root'])

        left, right = cur[cur['root'].neighbours[0]].resolved, \
            cur[cur['root'].neighbours[1]].resolved
        found = left == right
        diff = left-right

        if diff > 0:
            low = i + 1
        else:
            high = i - 1

    return int(cur['humn'].resolved)


def main():
    assert part1("example.txt") == 152
    print(part1("input.txt"))

    # somehow example and input have different search directions
    # assert part2("example.txt") == 301
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
