#!/usr/bin/env python3

import sys
import time
from collections import defaultdict, deque

from utils import io
from utils.parse import ints


def parse(lines):
    blueprints = []
    for line in lines:
        parts = line.split(": ")

        robots = parts[1].strip().split(" Each")
        costs = [ints(r) for r in robots]

        p = []
        p.append([costs[0][0], 0, 0, 0])
        p.append([costs[1][0], 0, 0, 0])
        p.append([costs[2][0], costs[2][1], 0, 0])
        p.append([costs[3][0], 0, costs[3][1], 0])

        blueprints.append(p)

    return blueprints


def collect(state, counts):
    new_state = list(state)
    for j, c in enumerate(counts):
        new_state[j] += c

    return new_state


def can_build(state, cost):
    for i, c in enumerate(cost):
        if state[i] < c:
            return False

    return True


# my original code was a recursive dfs that was dead slow and had some bugs in pruning
# rewrote to bfs + added some pruning that I got tipped about
# not a good day
def find_geos(plan, time):
    maxes = [max(cost[i] for cost in plan)
             for i in range(len(plan))]
    maxes[3] = float('inf')
    q = deque([(time, (0, 0, 0, 0), (1, 0, 0, 0))])
    r = 0

    cache = defaultdict(lambda: -1)
    while len(q) > 0:
        time, state, counts = q.pop()

        r = max(r, state[3])

        # uppber bound pruning, from reddit
        theoretical_upper_bound = ((time + counts[3]) * (time + counts[3] + 1)) // 2 \
            - (counts[3] * (counts[3] + 1)) // 2 \
            + state[3]
        if theoretical_upper_bound <= r:
            continue

        # check if cache has larger value, also got tipped about this
        key = (time, state[:3], counts)
        if cache[key] >= state[3]:
            continue
        else:
            cache[key] = state[3]

        if time == 0:
            continue

        wait = False
        for i, c in enumerate(counts):
            # we have a robot this kind,
            # but we are waiting for more collection to be able to build something that depends on it
            #
            # lets see what happens in this branch if we wait for it
            # note: original code always added a wait-branch, this was very slow
            if c > 0 and state[i] < maxes[i]:
                wait = True
                break

        if wait:
            # only collect
            new_state = collect(state, counts)

            q.append((time - 1, tuple(new_state), tuple(counts)))

        for i, cost in enumerate(plan):
            # never build a robot if the existing will produce in one turn what we need to build anything
            # otherwise check that we can build it
            if counts[i] < maxes[i] and can_build(state, cost):
                # collect
                new_state = collect(state, counts)
                # deduct cost of building
                for j, c in enumerate(cost):
                    new_state[j] -= c

                # build
                new_counts = list(counts)
                new_counts[i] += 1

                q.append((time - 1, tuple(new_state), tuple(new_counts)))
    return r


def play(p, t):
    t1 = time.time()
    print("trying", p)
    geo = find_geos(p, t)
    print("got", geo, "in %.2f" % (time.time() - t1), "seconds")
    print()

    return geo


def part1(filename):
    blueprints = parse(io.get_lines(filename))

    sum = 0
    for i, p in enumerate(blueprints):
        geo = play(p, 24)
        sum += geo * (i+1)

    return sum


def part2(filename):
    blueprints = parse(io.get_lines(filename))

    prod = 1
    for p in blueprints[:3]:
        geo = play(p, 32)
        prod *= geo

    return prod


def main():
    assert part1("example.txt") == 33
    print(part1("../input/2022/day19.txt"))

    assert part2("example.txt") == 3472
    print(part2("../input/2022/day19.txt"))


if __name__ == "__main__":
    sys.exit(main())
