from arenaMaker import YMazeArena, ArenaToYAML
import json


def makeArenas(path, n_arenas, n_agents):
    for n in range(n_arenas):
        time = 500
        corridor_width = ArenaToYAML.MAX_SIZE / 4
        y_wall_length=15
        y_angle=30
        random_colors = False
        y_maze = YMazeArena(n_agents, time, corridor_width, y_wall_length, y_angle, random_colors)

        file_name = f'{path}y_maze{n}.yaml'
        with open(file_name, 'w') as file:
            file.write(y_maze.makeYAML())
            print(f'Wrote arena to {file_name}')


def makeCurriculum(path, n_arenas):
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
    for n in range(n_arenas):
        file_name = f'y_maze{n}.yaml'
        learner[CONFIG_FILES].append(file_name)
        if n > 0:
            learner[THRESHOLDS].append(n / n_arenas)

    file_name = f'{path}Learner.json'
    with open(file_name, 'w') as file:
        file.write(json.dumps(learner))
        print(f'Wrote Learner to {file_name}')


if __name__ == '__main__':
    path = './configs/curriculums/y_maze/'
    n_arenas = 10
    n_agents = 9
    makeArenas(path, n_arenas, n_agents)
    makeCurriculum(path, n_arenas)