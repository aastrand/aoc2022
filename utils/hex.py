#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \

# https://www.redblobgames.com/grids/hexagons/#coordinates-cube
HEX_OFFSETS = {
    "n": (1, -1, 0),
    "s": (-1, 1, 0),
    "nw": (0, -1, 1),
    "ne": (1, 0, -1),
    "se": (0, 1, -1),
    "sw": (-1, 0, 1),
}


def hex_cube_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def hex_cube_subtract(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


# https://www.redblobgames.com/grids/hexagons/#distances
def hex_cube_dist(a, b):
    diff = hex_cube_subtract(a, b)
    return (abs(diff[0]) + abs(diff[1]) + abs(diff[2])) // 2
