import math
import random

class ArenaToYAML:

    MAX_SIZE = 40

    def __init__(self):
        self.arenas = []

    def addArena(self, time, items):
        self.arenas.append((time, items))

    def makeYAML(self):
        header = ['!ArenaConfig', 'arenas:']
        as_yaml = '\n'.join(header)

        for n in range(len(self.arenas)):
            arena = self.arenas[n]
            time = arena[0]
            items = arena[1]

            as_yaml += f'\n  {n}: !Arena'
            as_yaml += f'\n    t: {time}\n'

            item_yaml = ['    items:']
            for item in items:
                item_yaml.append('    - !Item')
                item_props = '      ' + '\n      '.join(item.makeYAML())
                item_yaml.append(item_props)
            as_yaml += '\n'.join(item_yaml)
        return as_yaml


class Item:

    NAMES = {'Agent', 'Wall', 'GoodGoal', 'BadGoal'}

    def __init__(self, name):
        if name not in self.NAMES:
            raise ValueError(f'{name} is not a valid item. Select from {self.NAMES}')
        self.name = name
        self.colors = []
        self.positions = []
        self.rotations = []
        self.sizes = []

    def addColor(self, r=153, g=153, b=153, random_color=False):
        # default to grey
        if random_color:
            r = -1
            g = -1 
            b = -1
        self.colors.append(f'- !RGB {{r: {r}, g: {g}, b: {b}}}')

    def addPosition(self, x, y, z):
        self.addVec3(self.positions, x, y, z)

    def addSize(self, x, y, z):
        self.addVec3(self.sizes, x, y, z)

    def addRotation(self, deg):
        self.rotations.append(deg)

    def addVec3(self, container: list, x, y, z):
        container.append(f'- !Vector3 {{x: {x}, y: {y}, z: {z}}}')

    def makeYAML(self):
        yaml_list = []
        yaml_list.append(f'name: {self.name}')

        if self.positions:
            yaml_list.append(f'positions:')
            for position in self.positions:
                yaml_list.append(position)

        if self.sizes:
            yaml_list.append(f'sizes:')
            for size in self.sizes:
                yaml_list.append(size)

        if self.colors:
            yaml_list.append(f'colors:')
            for color in self.colors:
                yaml_list.append(color)

        if self.rotations:
            yaml_list.append(f'rotations: {str(self.rotations)}')

        return yaml_list


class YMazeArena:

    WALL_THICKNESS = 0.2
    WALL_HEIGHT = 7

    def __init__(self, n_arenas, time, corridor_width, y_wall_length, y_angle, random_colors):
        self.n_arenas = n_arenas
        self.corridor_width = corridor_width
        self.y_wall_length = y_wall_length
        self.y_angle = y_angle
        self.random_colors = random_colors
        self.arenas = ArenaToYAML()
        for _ in range(n_arenas):
            items = self.makeItems()
            self.arenas.addArena(time, items)

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
        z = (ArenaToYAML.MAX_SIZE - self.y_wall_length) / 2
        y = 1

        walls.addPosition(x, y, z)
        walls.addRotation(0)
        walls.addSize(self.corridor_width - 0.5, 0.5, z * 2 - 0.5)
        walls.addColor(random_color=self.random_colors)

    def makeYWalls(self, walls):
        length = self.y_wall_length
        x = ArenaToYAML.MAX_SIZE/2
        z = ArenaToYAML.MAX_SIZE - length
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
        max_size = ArenaToYAML.MAX_SIZE
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
        delta_x = delta_x * random.choice([1, -1]) # randomize start of good/bad goal
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

    def makeYAML(self):
        return self.arenas.makeYAML()


class BaselineArena:

    def __init__(self, n_arenas, time):
        self.arena = ArenaToYAML()
        items = [Item('GoodGoal'), Item('BadGoal')]
        self.arena.addArena(time, items)

    def makeYAML(self):
        return self.arena.makeYAML()



if __name__ == '__main__':
    n_arenas = 5
    time = 500
    corridor_width = ArenaToYAML.MAX_SIZE / 4
    y_wall_length=15
    y_angle=30
    random_colors = False
    y_maze = YMazeArena(n_arenas, time, corridor_width, y_wall_length, y_angle, random_colors)
    print(y_maze.makeYAML())
