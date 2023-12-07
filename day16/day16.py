#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io
from utils.graph import floyd_warshall


# original slow code
def _find_pressure(cur, time, opened, graph, flow, dist):
    # cached = CACHE.get((cur, tuple(sorted(opened.keys()))))
    # if cached:
    #    return cached

    if time > 30:
        return (-1, {})

    pressure = 0
    if flow[cur] > 0 and cur not in opened:
        opened[cur] = time
        time += 1
        pressure = flow[cur] * (30 - time)

    candidates = list(filter(lambda n: n not in opened and flow[n] > 0, [
        n for n in graph.keys()]))

    global_max = 0
    global_opened = None
    for c in candidates:
        local_max, local_opened = _find_pressure(
            c, time+dist[(cur, c)], dict(opened), graph, flow, dist)
        if local_max > global_max:
            global_max = local_max
            global_opened = local_opened

    if global_opened:
        for k, v in global_opened.items():
            opened[k] = v

    r = (pressure + global_max, opened)
    # CACHE[(cur, tuple(sorted(opened.keys())))] = r
    return r


def _score(opened, total_time, flow):
    total = 0
    for tick in range(1, total_time + 1):
        opened_now = list(filter(lambda t: t[1] < tick, [
                          n for n in opened.items()]))
        tick_total = 0
        for o in opened_now:
            tick_total += flow[o[0]]
        total += tick_total

    return total


def _part1(filename):
    flow, graph, dist = parse(io.get_lines(filename))

    _, opened = _find_pressure('AA', 1, {}, graph, flow, dist)

    return _score(opened, 30, flow)


def _find_pressure2(cur, time, opened, graph, flow, dist):
    # key = tuple(sorted(opened.keys()))
    # cached = CACHE.get((cur, key))
    # if cached:
    #    return cached

    if time[0] > 26 or time[1] > 26:
        return (0, None)

    pressure = 0

    if time[0] <= time[1]:
        mover = 0
    else:
        mover = 1

    t = time[mover]
    if flow[cur[mover]] > 0 and cur[mover] not in opened:
        opened[cur[mover]] = t
        t += 1
        pressure = flow[cur[mover]] * (26 - t)

    candidates = list(filter(lambda n: n not in opened and flow[n] > 0, [
        n for n in graph.keys()]))

    global_max = 0
    global_opened = None
    for c in candidates:
        new_cur = (c, cur[1]) if mover == 0 else (cur[0], c)
        new_time = (t + dist[(cur[mover], c)], time[1]
                    ) if mover == 0 else (time[0], t + dist[(cur[mover], c)])
        local_max, local_opened = _find_pressure2(
            new_cur, new_time, dict(opened), graph, flow, dist)
        if local_max > global_max:
            global_max = local_max
            global_opened = local_opened

    if global_opened:
        for k, v in global_opened.items():
            opened[k] = v

    val = pressure + global_max
    # key = tuple(sorted(opened.keys()))

    r = (val, opened)
    # CACHE[((cur[0], cur[1]), key)] = r
    # CACHE[((cur[1], cur[0]), key)] = r
    return r


def parse(lines):
    flow = {}
    graph = defaultdict(list)

    for line in lines:
        parts = line.split("; ")
        valve = parts[0].split(" ")

        id = valve[1]
        pressure = int(valve[4].split("=")[1])
        if pressure > 0:
            flow[id] = pressure

        splitword = "valves " if "valves" in parts[1] else "valve "
        neighbours = parts[1].split(splitword)[1].split(", ")
        graph[id].extend(neighbours)

    dist = floyd_warshall(graph)

    return flow, graph, dist


# dave russels brilliant order generator
def generate_orders(dist, node, todo, done, time):
    for next_node in todo:
        cost = dist[(node, next_node)] + 1
        if cost < time:
            yield from generate_orders(dist, next_node, todo - {next_node},
                                       done + [next_node], time - cost)
    yield done


def score(dist, order, flow, t):
    pressure = 0

    for i in range(len(order)-1):
        cost = dist[(order[i], order[i+1])] + 1
        t -= cost
        pressure += t * flow.get(order[i+1], 0)

    return pressure


def part1(filename):
    flow, _, dist = parse(io.get_lines(filename))

    start = 'AA'
    orders = generate_orders(dist, start, flow.keys(), [start], 30)

    s = 0
    for order in orders:
        s = max(s, score(dist, order, flow, 30))

    return s


# inspiration from https://github.com/davearussell
# my solution ^ was horrible
def part2(filename):
    flow, _, dist = parse(io.get_lines(filename))

    start = 'AA'
    # all orders, including incomplete ones
    orders = generate_orders(dist, start, flow.keys(), [start], 26)
    # scores, sent along set of the order to use later when comparing with elephant
    scores = [(score(dist, order, flow, 26), set(order))
              for order in orders]
    scores.sort(key=lambda x: -x[0])

    s = 0
    # best score where we and elephant take entirely different paths
    for i, (score1, order1) in enumerate(scores):
        if score1 * 2 < s:
            # here we will already have found our best pair
            # rest of search will repeat pairs
            break

        for score2, order2 in scores[i+1:]:
            if order1 & order2 == set([start]):
                s = max(score1 + score2, s)

    return s


def main():
    assert part1("example.txt") == 1651
    print(part1("../input/2022/day16.txt"))

    assert part2("example.txt") == 1707
    print(part2("../input/2022/day16.txt"))


if __name__ == "__main__":
    sys.exit(main())
