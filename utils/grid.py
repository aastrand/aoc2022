from collections import namedtuple

RIGHT = (1, 0)
LEFT = (-1, 0)
BOTTOM = (0, 1)
TOP = (0, -1)
TOP_LEFT = (-1, -1)
BOTTOM_RIGHT = (1, 1)
TOP_RIGHT = (1, -1)
BOTTOM_LEFT = (-1, 1)


OFFSETS = (RIGHT, LEFT, BOTTOM, TOP, TOP_LEFT,
           BOTTOM_RIGHT, TOP_RIGHT, BOTTOM_LEFT)
OFFSETS_STRAIGHT = (RIGHT, LEFT, TOP, BOTTOM)


class Grid:
    def __init__(self):
        self.data = {}
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

    def set(self, coords, val):
        self.set_at(coords[0], coords[1], val)

    def set_at(self, x, y, val):
        self.minX = min(self.minX, x)
        self.maxX = max(self.maxX, x)
        self.minY = min(self.minY, y)
        self.maxY = max(self.maxY, y)
        self.data[(x, y)] = val

    def get(self, x, y):
        return self.data.get(x, y)

    def print(self, default="."):
        for y in range(self.minY, self.maxY+1):
            r = []
            for x in range(self.minX, self.maxX+1):
                r.append(str(self.data.get((x, y), default)))
            print("".join(r))
        print()


def flood_fill(grid, pos, visitor):
    q = [pos]
    visited = set()
    visited.add(pos)

    while len(q) > 0:
        pos = q.pop(0)
        visitor(grid, pos)

        for o in OFFSETS_STRAIGHT:
            neighbour = (pos[0] + o[0], pos[1] + o[1])
            if grid.get(neighbour) == "#" and neighbour not in visited:
                q.append(neighbour)
                visited.add(neighbour)