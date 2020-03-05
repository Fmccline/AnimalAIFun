import math
import random
from arenaToYaml import ArenaToYAML, Item

class YMazeArena(ArenaToYAML):

    WALL_THICKNESS = 0.2
    WALL_HEIGHT = 7

    def __init__(self, n_arenas, time, corridor_width, y_wall_length, y_angle, end_left, random_colors):
        super().__init__()
        self.corridor_width = corridor_width
        self.y_wall_length = y_wall_length
        self.y_angle = y_angle
        self.end_left = end_left
        self.random_colors = random_colors
        for _ in range(n_arenas):
            items = self.makeItems()
            self.addArena(time, items)

    def makeItems(self):
        walls = self.makeWalls()
        goals = self.makeGoals()
        agent = self.makeAgent()
        return walls + goals + agent

    def makeWalls(self):
        walls = Item('Wall')
        self.makeYWalls(walls)
        self.makeCorridorWalls(walls)
        self.makeFloor(walls)
        return [walls]

    def makeFloor(self, walls):
        x = 20
        z = (self.MAX_SIZE - self.y_wall_length) / 2
        y = 1

        walls.addPosition(x, y, z)
        walls.addRotation(0)
        walls.addSize(self.corridor_width - 0.5, 0.5, z * 2 - 0.5)
        walls.addColor(random_color=self.random_colors)

    def makeYWalls(self, walls):
        length = self.y_wall_length
        x = self.MAX_SIZE/2
        z = self.MAX_SIZE - length
        y = 0
        rotations = [90 - self.y_angle/2, 90 + self.y_angle/2]
        for rotation in rotations:
            self.addYWall(walls, x, y, z, length, rotation)

    def addYWall(self, walls, x, y, z, length, rotation):
        delta_x = math.cos(rotation * 2 * math.pi / 360) * length / 2 
        delta_z = math.sin(rotation * 2 * math.pi / 360) * length / 2

        thickness = self.WALL_THICKNESS
        delta_x = delta_x + thickness/2 if delta_x > 0 else delta_x - thickness/2

        walls.addPosition(x-delta_x, y, z+delta_z)
        walls.addRotation(rotation)
        walls.addSize(length, self.WALL_HEIGHT, thickness)
        walls.addColor(random_color=self.random_colors)

        if delta_x > 0:
            delta_x += self.corridor_width / 2
        else:
            delta_x -= self.corridor_width / 2
        walls.addPosition(x-delta_x, y, z+delta_z)
        walls.addRotation(rotation)
        walls.addSize(length, self.WALL_HEIGHT, thickness)
        walls.addColor(random_color=self.random_colors)

    def makeCorridorWalls(self, walls):
        max_size = self.MAX_SIZE
        half_size = max_size / 2
        length = max_size - self.y_wall_length
        xs = [half_size - self.corridor_width/2, half_size + self.corridor_width/2]
        z = length / 2
        y = 0
        for x in xs:
            walls.addPosition(x, y, z)
            walls.addRotation(0)
            walls.addSize(self.WALL_THICKNESS, self.WALL_HEIGHT, length)
            walls.addColor(random_color=self.random_colors)

    def makeGoals(self):
        delta_x = math.sin(self.y_angle/2 * 2*math.pi/360) * self.y_wall_length + self.corridor_width/4
        delta_x *= 1 if self.end_left else -1
        x = 20
        y = 0
        z = 38

        goodGoal = Item('GoodGoal')
        goodGoal.addPosition(x + delta_x, y, z)

        badGoal = Item('BadGoal')
        badGoal.addPosition(x - delta_x, y, z)
        return [goodGoal, badGoal]

    def makeAgent(self):
        agent = Item('Agent')
        agent.addPosition(20,1.5,1)
        agent.addRotation(0)
        return [agent]
