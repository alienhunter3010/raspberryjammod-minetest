from enum import Enum

import mcpi.minecraft as minecraft
from mcpi.block import *
from lib import server
from ast import literal_eval

from mcpi.vec3 import Vec3

PATTERN_MAP = {'_': BRICK_BLOCK,
               'W': BRICK_BLOCK,  # W for WALL, not for window
               'G': GLASS_PANE}


class Direction(Enum):
    NS = 0
    EW = 1


class OrientedBuild(Enum):
    NORTH = {
        "move": lambda v, front, height, wide: Vec3(v.x + front, v.y + height, v.z - wide),
        "put": lambda mc, front, height, wide, block: mc.setBlock(front, height, wide, block),
        "range-x": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.x, front),
        "range-z": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.z, wide),
        "straight": Direction.NS,
        "side": Direction.EW
    }
    WEST = {
        "move": lambda v, front, height, wide: Vec3(v.x - wide, v.y + height, v.z - front),
        "put": lambda mc, front, height, wide, block: mc.setBlock(wide, height, front, block),
        "range-x": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.x, wide),
        "range-z": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.z, front),
        "straight": Direction.EW,
        "side": Direction.NS
    }
    SOUTH = {
        "move": lambda v, front, height, wide: Vec3(v.x - front, v.y + height, v.z + wide),
        "put": lambda mc, front, height, wide, block: mc.setBlock(front, height, wide, block),
        "range-x": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.x, front),
        "range-z": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.z, wide),
        "straight": Direction.NS,
        "side": Direction.EW
    }
    EAST = {
        "move": lambda v, front, height, wide: Vec3(v.x + wide, v.y + height, v.z + front),
        "put": lambda mc, front, height, wide, block: mc.setBlock(wide, height, front, block),
        "range-x": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.x, wide),
        "range-z": lambda origin, front, height, wide: OrientedBuild.smart_range(origin.z, front),
        "straight": Direction.EW,
        "side": Direction.NS
    }

    @classmethod
    def smart_range(cls, start, end):
        return range(int(min(start, end)), int(max(start, end)))

    def move(self, v: Vec3, front=0, height=0, wide=0):
        return self.value["move"](v, front, height, wide)

    def bound(self, v: Vec3, front=1, height=1, wide=1):
        return self.move(v, front, height, wide)

    def solid(self, mc, origin: Vec3, target: Vec3, block=AIR, pattern=False, direction=Direction.NS):
        if pattern:
            mc.postToChat("pattern is {}".format(pattern))
        for xx in OrientedBuild.smart_range(origin.x, target.x):
            for yy in OrientedBuild.smart_range(origin.y, target.y):
                for zz in OrientedBuild.smart_range(origin.z, target.z):
                    mc.setBlock(xx, yy, zz, block if not pattern else self.solve_pattern(pattern,
                        (max(origin.z, target.z) - zz if direction == Direction.NS else max(origin.x, target.x) - xx) -1, mc
                    )),

    def direction_straight(self):
        return self.value["straight"]

    def direction_side(self):
        return self.value["side"]

    def solve_pattern(self, pattern, pos, mc):
        mc.postToChat("Position: {}".format(pos))
        if pos >= len(pattern):
            return PATTERN_MAP['_']
        return PATTERN_MAP[pattern[pos]]


class Orientation(Enum):
    NORTH = 3  #   0
    WEST = 2   #  90
    SOUTH = 1  # 180
    EAST = 0   # 270

    @classmethod
    def get_by_degree(cls, rotation):
        return Orientation(int((rotation + 45) / 90) % 4)

    def to_builder(self):
        if self == Orientation.NORTH:
            return OrientedBuild.NORTH
        elif self == Orientation.WEST:
            return OrientedBuild.WEST
        elif self == Orientation.SOUTH:
            return OrientedBuild.SOUTH
        elif self == Orientation.EAST:
            return OrientedBuild.EAST


class Payload:
    def __init__(self):
        self.mc = minecraft.Minecraft.create(server.address)
        self.builder = Orientation.get_by_degree(self.mc.player.getRotation()).to_builder()
        self.origin = self.mc.player.getPos()

        self.masonry = BRICK_BLOCK
        self.window = GLASS_PANE

    def warp(self, start=False, x=1, y=1, z=1, block=0, pattern=False):
        if not start:
            start = self.origin
        if not isinstance(block, Block):
            block = self.masonry
        for xx in range(0, int(x), int(x/abs(x))):
            for yy in range(0, int(y), int(y/abs(y))):
                for zz in range(0, int(z), int(z/abs(z))):
                    self.mc.setBlock(start.x + xx, start.y + yy, start.z + zz,
                                     block if not pattern else self.solve_pattern(pattern, abs(zz)))

    def solve_pattern(self, pattern, pos):
        if pos >= len(pattern):
            return self.masonry
        # W for WALL, not for window
        return self.masonry if pattern[pos] == 'W' else self.window

    def solve_block(self, name):
        try:
            return literal_eval(name)
        except:
            return globals()[name.upper()]

    def debug(self, msg):
        self.mc.postToChat(msg)