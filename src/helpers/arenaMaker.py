from arenaToYaml import ArenaToYAML
from yMazeArena import YMazeArena
from tMazeArena import TMazeArena
from radialMaze import RadialMaze
import argparse


class ArenaMaker:

    MAX_SIZE = ArenaToYAML.MAX_SIZE

    def __init__(self, n_arenas, time):
        self.n_arenas = n_arenas
        self.time = time
        self.num_made = 0

    def make_t_maze_arena(self):
        n_arenas = self.n_arenas
        time = self.time
        t_width = self.MAX_SIZE / 3
        t_height = self.MAX_SIZE*2/3
        div_height = t_height
        end_left = True if self.num_made % 2 == 0 else False
        random_colors = False
        arena = TMazeArena(n_arenas, time, t_width, t_height, div_height, end_left, random_colors)
        return arena

    def make_y_maze_arena(self):
        n_arenas = self.n_arenas
        time = self.time
        corridor_width = self.MAX_SIZE / 4
        y_wall_length=15
        y_angle=30
        end_left = True if self.num_made % 2 == 0 else False
        random_colors = False
        arena = YMazeArena(n_arenas, time, corridor_width, y_wall_length, y_angle, end_left, random_colors)
        return arena

    def make_radial_maze(self):
        n_arenas = self.n_arenas
        time = self.time
        arm_width = 5
        arm_length = 12
        random_colors = False
        arena = RadialMaze(n_arenas, time, arm_length, arm_width, random_colors)
        return arena

    def make_arena(self, arena_type):
        ARENAS = {
            't_maze': self.make_t_maze_arena,
            'y_maze': self.make_y_maze_arena,
            'radial_maze': self.make_radial_maze
        }
        if arena_type not in ARENAS.keys():
            raise ValueError(f'Invalid arena type {arena_type}')

        arena = ARENAS[arena_type]()
        self.num_made += 1
        return arena


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arena Maker for AnimalAI')
    parser.add_argument('-a', '--arena_type', dest='arena_type', default='t_maze', help='Type of arena to make i.e., "t_maze", "y_maze", or "radial_maze"')
    args = parser.parse_args()

    n_arenas = 1
    time = 1000
    arena_maker = ArenaMaker(n_arenas, time)
    arena = arena_maker.make_arena(args.arena_type)
    print(arena.makeYAML())
