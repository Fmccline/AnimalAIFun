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

    NAMES = {'Agent', 'Wall', 'GoodGoal', 'BadGoal', 'GoodGoalMulti'}

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


class BaselineArena:

    def __init__(self, n_arenas, time):
        self.arena = ArenaToYAML()
        items = [Item('GoodGoal'), Item('BadGoal')]
        self.arena.addArena(time, items)

    def makeYAML(self):
        return self.arena.makeYAML()