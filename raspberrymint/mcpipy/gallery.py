#!/usr/bin/env python

import buildings.payload as payload
import sys
import math
import mcpi.block as block
from mcpi.vec3 import Vec3


class Gallery(payload.Payload):
    def __init__(self):
        payload.Payload.__init__(self)
        self.wall_height = int(sys.argv[1]) if len(sys.argv) >= 2 else 4
        self.height = int(sys.argv[2]) if len(sys.argv) >= 3 else 6
        self.wide = int(sys.argv[3]) if len(sys.argv) >= 4 else 12
        self.deep = int(sys.argv[4]) if len(sys.argv) >= 5 else 12

        self.wall_material = self.solve_block(sys.argv[5]) if len(sys.argv) >= 6 else block.BRICK_BLOCK
        self.roof_material = self.solve_block(sys.argv[6]) if len(sys.argv) >= 7 else block.OBSIDIAN_GLASS

        delta = self.height - self.wall_height
        self.radius = (4*delta**2+self.wide**2)/(8*delta)
        self.semi_roof = int(math.ceil(self.wide / 2))
        self.west = self.builder.move(self.origin, front=-self.semi_roof)
        self.east = self.builder.move(self.origin, front=(self.wide - self.semi_roof))
        self.west.iround()
        self.east.iround()

    def delta_height(self, x):
        return round(self.radius - math.sqrt(self.radius**2-x**2))

    def box(self, roof_point):
        pass

    def on_success(self):
        self.mc.postToChat("Gallery ready")

    def wall(self, start):
        self.builder.solid(self.mc, start,
                    self.builder.bound(start, height=self.wall_height, wide=self.deep),
                    self.wall_material)

    def run(self):
        # Walls
        self.wall(self.west)
        self.wall(self.east)

        # Roof
        west = self.west.clone()
        east = self.east.clone()
        for x in range(self.semi_roof, -1, -1):
            y = self.height - self.delta_height(x)
            west.y = east.y = self.origin.y + y
            # self.warp(start=west, z=self.deep, block=self.roof_material)
            # self.warp(start=east, z=self.deep, block=self.roof_material)
            self.builder.solid(self.mc, west,
                        self.builder.bound(west, wide=self.deep),
                        self.roof_material)
            self.builder.solid(self.mc, east,
                        self.builder.bound(east, wide=self.deep),
                        self.roof_material)


            self.box(west)
            self.box(east)
            #west.x += 1
            #east.x -= 1
            west = self.builder.move(west, front=1)
            east = self.builder.move(east, front=-1)

        self.on_success()


if __name__ == "__main__":
    o = Gallery()
    o.run()
