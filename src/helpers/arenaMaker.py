import math
import random
from arenaToYaml import ArenaToYAML
from yMazeArena import YMazeArena
from tMazeArena import TMazeArena
import argparse

parser = argparse.ArgumentParser(description='Arena Maker for AnimalAI')
parser.add_argument('-a', '--arena', dest='arena_type', default='t_maze', help='Type of arena to make.')
args = parser.parse_args()


if __name__ == '__main__':
    max_size = ArenaToYAML.MAX_SIZE
    arena = None
    if args.arena_type == 't_maze':
        n_arenas = 1
        time = 500
        t_width = max_size / 3
        t_height = max_size*2/3
        div_height = t_height
        random_colors = False
        arena = TMazeArena(n_arenas, time, t_width, t_height, div_height, random_colors)
    elif args.arena == 'y_maze':
        n_arenas = 5
        time = 500
        corridor_width = max_size / 4
        y_wall_length=15
        y_angle=30
        random_colors = False
        arena = YMazeArena(n_arenas, time, corridor_width, y_wall_length, y_angle, random_colors)
    print(arena.makeYAML())
