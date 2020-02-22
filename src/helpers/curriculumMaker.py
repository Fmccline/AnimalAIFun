from yMazeArena import YMazeArena
from tMazeArena import TMazeArena
from arenaToYaml import ArenaToYAML
import json

def makeArena(curriculum_type, n_arenas, time):
    arena = None
    random_colors = False
    if curriculum_type == 'y_maze':
        corridor_width = ArenaToYAML.MAX_SIZE / 4
        y_wall_length=15
        y_angle=30
        arena = YMazeArena(n_arenas, time, corridor_width, y_wall_length, y_angle, random_colors)
    elif curriculum_type == 't_maze':
        t_width = 10
        t_height = 20
        div_height = 20
        arena = TMazeArena(n_arenas, time, t_width, t_height, div_height, random_colors)
    else:
        raise ValueError(f'Invalid curriculum type {curriculum_type}')
    return arena

def makeArenas(path, curriculum_type, n_files, n_arenas, time):
    for n in range(n_files):
        arena = makeArena(curriculum_type, n_arenas, time)
        file_name = f'{path}{curriculum_type}{n}.yaml'
        with open(file_name, 'w') as file:
            file.write(arena.makeYAML())
            print(f'Wrote arena to {file_name}')


def makeCurriculum(path, curriculum_type, n_files):
    MEASURE = 'measure'
    THRESHOLDS = 'thresholds'
    CONFIG_FILES = 'configuration_files'
    MIN_LESSON_LEN = 'min_lesson_length'
    SIGNAL_SMOOTHING = 'signal_smoothing'
    learner = {}
    learner[MIN_LESSON_LEN] = 100
    learner[SIGNAL_SMOOTHING] = True
    learner[MEASURE] = 'progress'
    learner[THRESHOLDS] = []
    learner[CONFIG_FILES] = []
    for n in range(n_files):
        file_name = f'{curriculum_type}{n}.yaml'
        learner[CONFIG_FILES].append(file_name)
        if n > 0:
            learner[THRESHOLDS].append(n / n_files)

    file_name = f'{path}Learner.json'
    with open(file_name, 'w') as file:
        file.write(json.dumps(learner))
        print(f'Wrote Learner to {file_name}')


import argparse

parser = argparse.ArgumentParser('Curriculum maker')
parser.add_argument('-c', '--curriculum', help='Type of curriculum to make')
parser.add_argument('-n', '--num_arenas', help='Number of arenas per file.', type=int)
parser.add_argument('-f', '--num_files', help='Number of files to make.', type=int)
parser.add_argument('-t', '--time', help='Time limit of each arena.', type=int, default=500)

args = parser.parse_args()


if __name__ == '__main__':

    curriculum = args.curriculum
    num_arenas = args.num_arenas
    num_files = args.num_files
    time = args.time

    path = f'./configs/curriculums/{curriculum}/'
    makeArenas(path, curriculum, num_files, num_arenas, time)
    makeCurriculum(path, curriculum, num_files)
