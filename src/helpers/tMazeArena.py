import math
import random
from arenaToYaml import ArenaToYAML, Item

class TMazeArena(ArenaToYAML):

    WALL_THICKNESS = 0.2
    WALL_HEIGHT = 7

    def __init__(self, n_arenas, time, t_width, t_height, div_height, end_left, random_colors):
        super().__init__()
        self.t_width = t_width
        self.t_height = t_height
        self.div_height = div_height
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
        self.makeUpperT(walls)
        self.makeMidDivider(walls)
        self.makeLeftDivider(walls)
        self.makeRightDivider(walls)
        return [walls]

    def makeUpperT(self, walls):
        size = self.MAX_SIZE
        x = self.MAX_SIZE/2
        z = self.MAX_SIZE - self.WALL_THICKNESS
        y = 0
        rotation = 0
        self.addWall(walls, x, y, z, size, rotation)

    def makeMidDivider(self, walls):
        size = self.div_height
        x = self.MAX_SIZE/2
        z = self.MAX_SIZE - size/2 - self.WALL_THICKNESS*2
        y = 0
        rotation = 90
        self.addWall(walls, x, y, z, size, rotation)

    def makeLeftDivider(self, walls):
        xl = (self.MAX_SIZE - self.t_width) / 2
        zl = self.t_height
        x = xl / 2
        z = zl / 2
        y = 0
        self.addFilledWall(walls, x, y, z, xl, zl)

    def makeRightDivider(self, walls):
        xl = (self.MAX_SIZE - self.t_width) / 2
        zl = self.t_height
        x = self.MAX_SIZE - xl / 2
        z = zl / 2
        y = 0
        self.addFilledWall(walls, x, y, z, xl, zl)

    def addWall(self, walls, x, y, z, size, rotation):
        walls.addPosition(x, y, z)
        walls.addRotation(rotation)
        walls.addSize(size, self.WALL_HEIGHT, self.WALL_THICKNESS)
        walls.addColor(random_color=self.random_colors)

    def addFilledWall(self, walls, x, y, z, xl, zl):
        walls.addPosition(x, y, z)
        walls.addRotation(0)
        walls.addSize(xl, self.WALL_HEIGHT, zl)
        walls.addColor(random_color=self.random_colors)

    def makeGoals(self):
        offset = 3
        goalPositions = [offset, self.MAX_SIZE - offset]
        goodPos = goalPositions[0] if self.end_left else goalPositions[1]
        badPos = goalPositions[0] if goalPositions[0] != goodPos else goalPositions[1]
        zPos= self.t_height + (self.MAX_SIZE - self.t_height)/2
        
        goodGoal = Item('GoodGoal')
        goodGoal.addPosition(goodPos, 0, zPos)
        goodGoal.addRotation(0)

        badGoal = Item('BadGoal')
        badGoal.addPosition(badPos, 0, zPos)
        badGoal.addRotation(0)

        return [goodGoal, badGoal]

    def makeAgent(self):
        agent = Item('Agent')
        agent.addPosition(20,1.5,1)
        agent.addRotation(0)
        return [agent]
