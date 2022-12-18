import unittest

from utils.hex import (HEX_OFFSETS, hex_cube_add, hex_cube_dist,
                       hex_cube_subtract)


class TestHex(unittest.TestCase):

    def test_add(self):
        result = hex_cube_add((0, 0, 0), HEX_OFFSETS["n"])
        self.assertEqual((1, -1, 0), result)

    def test_subtract(self):
        result = hex_cube_subtract((0, 0, 0), HEX_OFFSETS["n"])
        self.assertEqual(HEX_OFFSETS["s"], result)

    def test_dist(self):
        result = hex_cube_dist(HEX_OFFSETS["sw"], HEX_OFFSETS["ne"])
        self.assertEqual(2, result)
