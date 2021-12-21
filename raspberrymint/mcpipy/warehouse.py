from buildings.sym_wall import WindowedWall
from gallery import Gallery


class Warehouse(Gallery):

    def __init__(self):
        Gallery.__init__(self)
        ww = WindowedWall(self.deep)
        self.pattern = ww.build()

    def box(self, roof_point):
        self.builder.solid(self.mc, roof_point,
                    self.builder.bound(roof_point, height=self.origin.y - roof_point.y),
                    self.wall_material)
        column = self.builder.move(roof_point, wide=self.deep - 1)
        self.builder.solid(self.mc, column,
                    self.builder.bound(column, height=self.origin.y - roof_point.y),
                    self.wall_material)

    def wall(self, start):
        super().wall(start)
        for y in range(2, self.wall_height -2, 4):
            start_point = self.builder.move(start, height=y)
            self.builder.solid(self.mc, start_point,
                               self.builder.bound(start_point, height=2, wide=self.deep),
                               pattern=self.pattern, direction=self.builder.direction_straight())

    def on_success(self):
        self.mc.postToChat("Warehouse ready")
        self.mc.postToChat("Dig the door by yourself")


if __name__ == "__main__":
    o = Warehouse()
    o.run()
