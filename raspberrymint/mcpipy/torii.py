import buildings.payload as payload
import sys
import math
import mcpi.block as block
from mcpi.block import Block


class Torii(payload.Payload):
    def __init__(self):
        payload.Payload.__init__(self)
        self.height = int(sys.argv[1]) if len(sys.argv) >= 2 else 6
        self.wide = int(sys.argv[2]) if len(sys.argv) >= 3 else 4
        self.tickness = int(sys.argv[3]) if len(sys.argv) >= 4 else 1

        self.vertical_material = self.solve_block(sys.argv[4]) if len(sys.argv) >= 5 else Block(block.FENCE.id, 4)
        self.roof_material = self.solve_block(sys.argv[5]) if len(sys.argv) >= 6 else Block(block.WOOD_SLAB.id, 3)
        self.horizontal_material = self.solve_block(sys.argv[6]) if len(sys.argv) >= 7 else Block(block.FENCE_RAIL.id, 4)

        self.semi_wide = int(math.ceil(self.wide / 2))
        self.west = self.builder.move(self.origin, front=-self.semi_wide)
        self.east = self.builder.move(self.origin, front=(self.wide - self.semi_wide))

    def on_success(self):
        self.mc.postToChat("Torii ready")

    def column(self, start):
        candidate = self.builder.bound(start, self.tickness, self.height, self.tickness)
        self.builder.solid(self.mc, start, candidate, self.vertical_material)

    def run(self):
        # Columns
        self.column(self.west)
        self.column(self.east)

        # Roof
        west = self.builder.move(self.west, front=self.tickness, height=self.height -1)
        self.builder.solid(self.mc, west,
                        self.builder.bound(west, front=self.wide - self.tickness, wide=self.tickness),
                        self.horizontal_material)
        west = self.builder.move(self.west, height=self.height)
        self.builder.solid(self.mc, west,
                        self.builder.bound(west, front=self.wide + self.tickness, wide=self.tickness),
                        self.roof_material)

        self.on_success()


if __name__ == "__main__":
    o = Torii()
    o.run()
