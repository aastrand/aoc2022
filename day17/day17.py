#!/usr/bin/env python3

import copy
import sys
from dataclasses import dataclass

from utils import io
from utils.grid import Grid


@dataclass
class Shape:
    minX: int
    maxX: int
    minY: int
    maxY: int
    coords: list

    def add_to_grid(self, grid, pos, default='#'):
        for c in self.coords:
            grid.set((pos[0] + c[0], pos[1] + c[1]), default)

    def intersects(self, grid, pos):
        for c in self.coords:
            if grid.get((pos[0] + c[0], pos[1] + c[1])) is not None:
                return True

        return False


# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:


SHAPES = [
    # ####
    Shape(
        0, 3, 0, 0,
        [(0, 0), (1, 0), (2, 0), (3, 0)]
    ),

    # .#.
    # ###
    # .#.
    Shape(
        0, 2, -2, 0,
        [(1, -2),
         (0, -1), (1, -1), (2, -1),
         (1, 0)
         ]
    ),

    # ..#
    # ..#
    # ###
    Shape(
        0, 2, -2, 0,
        [(2, -2),
         (2, -1),
         (0, 0), (1, 0), (2, 0)
         ]
    ),

    # #
    # #
    # #
    # #
    Shape(
        0, 0, -3, 0,
        [(0, -3),
         (0, -2),
         (0, -1),
         (0, 0)
         ]
    ),

    # ##
    # ##
    Shape(
        0, 1, -1, 0,
        [(0, -1), (1, -1),
         (0, 0), (1, 0)
         ]
    ),
]


def get_input(filename):
    return io.get_input(filename).strip()


def start_pos(grid, _):
    return [2, (grid.minY - 4)]


def blow_rock(grid, rock, pos, direction):
    offset = -1 if direction == '<' else 1

    new_x = pos[0] + offset
    new_x = max(0, new_x)
    new_x = min(6 - rock.maxX, new_x)
    if not rock.intersects(grid, (new_x, pos[1])):
        pos[0] = new_x

    return [pos[0], pos[1]]


def run_rocks(wind, rocks):
    wpos = 0

    grid = Grid()
    grid.set((-1, 0), '+')
    grid.set((7, 0), '+')
    for x in range(0, 7):
        grid.set((x, 0), '-')

    cache = {}
    skipped = 0

    i = 0
    while i < rocks:
        # Each rock appears so that its left edge is two units away from the left wall
        # and its bottom edge is three units above the highest rock in the room
        #  (or the floor, if there isn't one).
        rock = SHAPES[i % 5]
        pos = start_pos(grid, rock)

        # After a rock appears, it alternates between being pushed by a jet of hot gas one unit
        # (in the direction indicated by the next symbol in the jet pattern)
        # and then falling one unit down.
        j = 0
        while j % 2 == 0 or not (j % 2 == 1 and rock.intersects(grid, (pos[0], pos[1] + 1))):
            if j % 2 == 1:
                pos[1] += 1
            else:
                # move
                pos = blow_rock(grid, rock, pos, wind[wpos % len(wind)])
                wpos += 1

            j += 1

        rock.add_to_grid(grid, (pos[0], pos[1]))

        # detect cycles, skip lots of work
        key = (i % 5, wpos % len(wind), ''.join(
            grid.print_output_from(0, grid.maxX, grid.minY, grid.minY+10)))
        if key not in cache:
            cache[key] = (i, abs(grid.minY))
        elif skipped == 0:
            val = cache[key]
            cycle_length = i - val[0]
            cycle_height = abs(grid.minY) - val[1]

            skip = (rocks - i - 1) // cycle_length
            skipped = (skip * cycle_height)

            # print('cycle detected at', i, ', cycle length:',
            #      cycle_length, ', cycle height', cycle_height, ', skipping', skip * cycle_length, 'iterations for', skipped, 'extra height')
            i += (skip * cycle_length)

        i += 1

    return grid, abs(grid.minY) + skipped


def solve(filename, rocks):
    _, height = run_rocks(get_input(filename), rocks)

    return height


def main():
    grid = Grid()
    grid.set((0, 0), '+')

    # +###
    assert SHAPES[0].intersects(grid, (0, 0)) == True
    # +####
    assert SHAPES[0].intersects(grid, (1, 0)) == False
    # ###+
    assert SHAPES[0].intersects(grid, (-3, 0)) == True
    # ####+
    assert SHAPES[0].intersects(grid, (-4, 0)) == False
    # ####
    # +
    assert SHAPES[0].intersects(grid, (0, -1)) == False
    # +
    # ####
    assert SHAPES[0].intersects(grid, (0, 1)) == False
    # ####
    #    +
    assert SHAPES[0].intersects(grid, (-3, -1)) == False
    #    +
    # ####
    assert SHAPES[0].intersects(grid, (-3, 1)) == False

    #  +
    # ###
    #  #
    assert SHAPES[1].intersects(grid, (-1, 2)) == True

    #  #
    # ###
    #  +
    assert SHAPES[1].intersects(grid, (-1, 0)) == True

    #  #
    # +##
    #  #
    assert SHAPES[1].intersects(grid, (0, 1)) == True

    #  #
    # ##+
    #  #
    assert SHAPES[1].intersects(grid, (-2, 1)) == True

    #  #
    # ###
    # +#
    assert SHAPES[1].intersects(grid, (0, 0)) == False

    #  #+
    # ###
    #  #
    assert SHAPES[1].intersects(grid, (-2, 2)) == False

    # +#
    # ###
    #  #
    assert SHAPES[1].intersects(grid, (0, -2)) == False

    #  #
    # ###
    #  #+
    assert SHAPES[1].intersects(grid, (-2, 0)) == False

    expected = ['...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 1)
    assert grid.print_output() == expected

    expected = ['....#....',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 2)
    assert grid.print_output() == expected

    expected = ['...#.....',
                '...#.....',
                '.####....',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 3)
    assert start_pos(grid, SHAPES[3]) == [2, -10]
    assert grid.print_output() == expected

    expected = ['.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 4)
    assert start_pos(grid, SHAPES[4]) == [2, -11]
    assert grid.print_output() == expected

    expected = ['.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 5)
    assert start_pos(grid, SHAPES[0]) == [2, -13]
    assert grid.print_output() == expected

    expected = ['..####...',
                '.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 6)
    assert start_pos(grid, SHAPES[1]) == [2, -14]
    assert grid.print_output() == expected

    expected = ['...#.....',
                '..###....',
                '...#.....',
                '..####...',
                '.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 7)
    assert start_pos(grid, SHAPES[2]) == [2, -17]
    assert grid.print_output() == expected

    expected = ['......#..',
                '......#..',
                '...####..',
                '..###....',
                '...#.....',
                '..####...',
                '.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 8)
    assert start_pos(grid, SHAPES[3]) == [2, -19]
    assert grid.print_output() == expected

    expected = ['.....#...',
                '.....#...',
                '.....##..',
                '.....##..',
                '...####..',
                '..###....',
                '...#.....',
                '..####...',
                '.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 9)
    assert start_pos(grid, SHAPES[4]) == [2, -21]
    assert grid.print_output() == expected

    expected = ['.....#...',
                '.....#...',
                '.....##..',
                '.##..##..',
                '.######..',
                '..###....',
                '...#.....',
                '..####...',
                '.....##..',
                '.....##..',
                '.....#...',
                '...#.#...',
                '...#.#...',
                '.#####...',
                '...###...',
                '....#....',
                '...####..',
                '+-------+']
    grid, _ = run_rocks(get_input("example.txt"), 10)
    assert start_pos(grid, SHAPES[0]) == [2, -21]
    assert grid.print_output() == expected

    assert solve("example.txt", 2022) == 3068
    print(solve("input.txt", 2022))

    assert solve("example.txt", 1000000000000) == 1514285714288
    print(solve("input.txt", 1000000000000))


if __name__ == "__main__":
    sys.exit(main())
