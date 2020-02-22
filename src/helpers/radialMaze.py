import math
import random
from arenaToYaml import ArenaToYAML, Item

class RadialMaze(ArenaToYAML):

    WALL_THICKNESS = 0.2
    WALL_HEIGHT = 4

    def __init__(self, n_arenas, time, arm_length, arm_width, random_colors=False):
        super().__init__()
        self.arm_length = arm_length
        self.arm_width = arm_width
        self.random_colors = random_colors
        self.apothem = arm_width/(math.tan(45/2)*2)
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
        self.makeArms(walls)
        return [walls]

    def makeArms(self, walls):
        size = self.arm_length
        mid = self.MAX_SIZE / 2
        half_side = self.arm_width/2
        inside_offets = {
            0: {
                'x': [self.apothem]*2, 
                'y': [-1*half_side, half_side]
            },
            45: {
                'x': [self.apothem, half_side],
                'y': [half_side, self.apothem]
            },
            90: {
                'x': [half_side, -1*half_side],
                'y': [self.apothem]*2
            },
            135: {
                'x': [-1*half_side, -1*self.apothem],
                'y': [self.apothem, half_side]
            },
            180: {
                'x': [-1*self.apothem]*2,
                'y': [half_side, -1*half_side]
            },
            225: {
                'x': [-1*self.apothem, -1*half_side],
                'y': [-1*half_side, -1*self.apothem]
            },
            270: {
                'x': [-1*half_side, half_side],
                'y': [-1*self.apothem]*2
            },
            315: {
                'x': [half_side, self.apothem],
                'y': [-1*self.apothem, -1*half_side]
            }
        }
        for rotation, offsets in inside_offets.items():
            wall_offset = math.sqrt(self.WALL_THICKNESS) if rotation % 90 != 0 else self.WALL_THICKNESS
            x_offsets = offsets['x']
            y_offsets = offsets['y']

            rads = rotation*2*math.pi/360
            x_out = size/2*math.cos(rads)
            y_out = size/2*math.sin(rads)

            sign = lambda num : -1 if num < 0 else 1
            # make side walls
            x0 = mid + x_offsets[0] + wall_offset*sign(x_offsets[0]) + x_out
            x1 = mid + x_offsets[1] + wall_offset*sign(x_offsets[1]) + x_out
            y0 = mid + y_offsets[0] + wall_offset*sign(y_offsets[0]) + y_out
            y1 = mid + y_offsets[1] + wall_offset*sign(y_offsets[1]) + y_out
            self.addWall(walls, x0, 0, y0, size, rotation)
            self.addWall(walls, x1, 0, y1, size, rotation)
            # make end wall
            x2 = mid + (self.apothem + self.arm_length + self.WALL_THICKNESS)*math.cos(rads)
            y2 = mid + (self.apothem + self.arm_length + self.WALL_THICKNESS)*math.sin(rads)
            end_size = self.arm_width/2 if rotation % 90 != 0 else self.arm_width
            self.addWall(walls, x2, 0, y2, end_size, rotation+90)

    def addWall(self, walls, x, y, z, size, rotation):
        if rotation >= 360:
            rotation -= 360
        elif rotation < 0:
            rotation += 360
        rotation = 360 - rotation

        walls.addPosition(x, y, z)
        walls.addRotation(rotation)
        walls.addSize(size, self.WALL_HEIGHT, self.WALL_THICKNESS)
        walls.addColor(random_color=self.random_colors)

    def makeGoals(self):
        goals = []
        goal_names = ['GoodGoalMulti', 'GoodGoal', 'BadGoal', None]
        goal_offset = 3
        for rotation in range(0, 360, 45):
            rads = rotation*2*math.pi/360
            x = self.MAX_SIZE/2 + (self.apothem + self.arm_length - goal_offset)*math.cos(rads)
            y = self.MAX_SIZE/2 + (self.apothem + self.arm_length - goal_offset)*math.sin(rads)
            goal_name = random.choice(goal_names)
            if goal_name is not None:
                goal = Item(goal_name)
                goal.addPosition(x, 0, y)
                goals.append(goal)
        return goals

    def makeAgent(self):
        agent = Item('Agent')
        agent.addPosition(20,0,20)
        agent.addRotation(0)
        return [agent]
