import math

class ArenaToYAML:

    MAX_SIZE = 40

    def __init__(self, n_arenas=1, time=500):
        self.n_arenas = n_arenas
        self.time = time
        self.items = []

    def addItems(self, items):
        self.items += items

    def makeYAML(self):
        header = ['!ArenaConfig', 'arenas:']
        as_yaml = '\n'.join(header)

        for arena in range(self.n_arenas):
            as_yaml += f'\n  {arena}: !Arena'
            as_yaml += f'\n    t: {self.time}\n'

            item_yaml = ['    items:']
            for item in self.items:
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
        self.positions = []
        self.rotations = []
        self.sizes = []

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

        if self.rotations:
            yaml_list.append(f'rotations: {str(self.rotations)}')

        return yaml_list


class YMazeArena:


    def __init__(self, y_wall_length, y_angle):
        self.y_wall_length = y_wall_length
        self.y_angle = y_angle
        self.arena = ArenaToYAML()
        items = self.makeItems()
        self.arena.addItems(items)

    def makeItems(self):
        walls = self.makeYWalls()
        goals = self.makeGoals()
        agent = self.makeAgent()
        return walls + goals + agent

    def makeYWalls(self):
        length = self.y_wall_length
        x = ArenaToYAML.MAX_SIZE / 2
        z = ArenaToYAML.MAX_SIZE-length
        y = 0
        thickness = 0.2
        rotations = [90 - self.y_angle/2, 90 + self.y_angle/2]
        walls = Item('Wall')
        for rotation in rotations:
            self.addYWall(walls, x, y, z, length, thickness, rotation)
        return [walls]

    def addYWall(self, walls, x, y, z, length, thickness, rotation):
        delta_x = math.cos(rotation * 2 * math.pi / 360) * length / 2 
        delta_z = math.sin(rotation * 2 * math.pi / 360) * length / 2

        delta_x = delta_x + thickness/2 if delta_x > 0 else delta_x - thickness/2

        walls.addPosition(x-delta_x, y, z+delta_z)
        walls.addRotation(rotation)
        walls.addSize(length, 5, thickness)

    def makeGoals(self):
        goodGoal = Item('GoodGoal')
        badGoal = Item('BadGoal')
        return [goodGoal, badGoal]

    def makeAgent(self):
        agent = Item('Agent')
        agent.addPosition(20,0,1)
        return [agent]

    def makeYAML(self):
        return self.arena.makeYAML()


if __name__ == '__main__':
    y_maze = YMazeArena(30, 30)
    print(y_maze.makeYAML())