#!/usr/bin/env python3

import sys
from collections import deque
from dataclasses import dataclass
from functools import reduce

from utils import io
from utils.parse import ints


def debug(s):
    pass
    # print(s)


@dataclass
class Monkey:
    id: int
    items: list
    op: str
    divisor: int
    to: dict
    count: int = 0

    def operation(self, x):
        if "old * old" in self.op:
            r = x * x
            debug("    Worry level is multiplied by itself to %s." % r)
            return r
        elif "old *" in self.op:
            r = x * ints(self.op)[0]
            debug("    Worry level is multiplied by %s to %s." %
                  (ints(self.op)[0], r))
            return r
        elif "old +" in self.op:
            r = x + ints(self.op)[0]
            debug("    Worry level increases by to %s." % r)
            return r
        else:
            print("undefined op", self.op)
            quit()

    def test(self, arg):
        return arg % self.divisor == 0


def round(monkeys, total=0):
    for c in range(0, len(monkeys)):
        m = monkeys[c]
        debug("Monkey %s :" % m.id)

        while m.items:
            m.count += 1

            item = m.items.popleft()
            debug("  Monkey inspects an item with a worry level of %d." % item)
            item = m.operation(item)

            if total > 0:
                item = item % total
            else:
                item = item // 3

            debug(
                "    Monkey gets bored with item. Worry level is divided by 3 to %d." % item)
            outcome = m.test(item)
            if outcome:
                debug("    Current worry level is divisible by %d." %
                      m.divisor)
            else:
                debug("    Current worry level is not divisible by %d." %
                      m.divisor)

            to = m.to[outcome]
            debug("    Item with worry level %d is thrown to monkey %s." %
                  (item, to))
            monkeys[to].items.append(item)


def parse(input):
    monkeys = {}
    for m in input:
        parts = m.split("\n")
        id = ints(parts[0])[0]
        items = deque(ints(parts[1]))
        op = parts[2]
        divisor = ints(parts[3])[0]

        to = {
            True: ints(parts[4])[0],
            False: ints(parts[5])[0],
        }
        monkeys[id] = Monkey(id, items, op, divisor, to)

    return monkeys


def score(monkeys):
    counts = [m.count for m in monkeys.values()]
    counts.sort()

    return counts[len(counts) - 2] * counts[len(counts) - 1]


def part1(filename):
    monkeys = parse(io.get_input(filename).split("\n\n"))

    for r in range(0, 20):
        round(monkeys, 0)

    return score(monkeys)


def part2(filename):
    monkeys = parse(io.get_input(filename).split("\n\n"))

    product = reduce((lambda x, y: x * y),
                     [m.divisor for m in monkeys.values()])
    samples = set([1, 20] + [i * 1000 for i in range(1, 11)])

    for r in range(0, 10000):
        round(monkeys, product)

        if r + 1 in samples:
            debug("== After round %d ==" % (r+1))
            for m in range(0, len(monkeys)):
                debug("Monkey %d inspected items %d times." %
                      (m, monkeys[m].count))

    return score(monkeys)


def main():
    assert part1("example.txt") == 10605
    print(part1("input.txt"))

    assert part2("example.txt") == 2713310158
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
