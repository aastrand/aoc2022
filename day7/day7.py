#!/usr/bin/env python3

from utils import io
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def find_sizes(tree, cur):
    size = 0
    for f in cur["files"]:
        size += f[1]

    for c in cur["children"]:
        child_size = find_sizes(tree, tree[cur["name"] + "/" + c])
        size += child_size

    cur["size"] = size

    return size


def parse(lines):
    tree = {}
    cur = None
    path = []

    for line in lines:
        parts = line.split(" ")
        if parts[0] == "$":
            if parts[1] == "cd":
                if parts[2] == "..":
                    if cur["parent"]:
                        cur = cur["parent"]
                        path.pop()
                else:
                    path.append(parts[2])
                    path_name = "/".join(path)

                    if path_name not in tree:
                        cur = {"name": path_name, "children": [],
                               "parent": cur, "files": []}
                        tree[path_name] = cur
                    else:
                        cur = tree[path_name]
        elif parts[0] == "dir":
            cur["children"].append(parts[1])
        else:
            cur["files"].append((parts[1], int(parts[0])))

    find_sizes(tree, tree["/"])

    return tree


def part1(filename):
    tree = parse(io.get_lines(filename))

    sum = 0
    for name, dir in tree.items():
        if dir["size"] <= 100000:
            sum += dir["size"]

    return sum


def part2(filename):
    tree = parse(io.get_lines(filename))

    total = 70000000
    needed = 30000000
    used = tree["/"]["size"]

    min = total
    for name, dir in tree.items():
        if (total-used) + dir["size"] > needed and min > dir["size"]:
            min = dir["size"]

    return min


def main():
    assert part1("example.txt") == 95437
    print(part1("input.txt"))

    assert part2("example.txt") == 24933642
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
