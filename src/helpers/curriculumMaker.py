from arenaMaker import ArenaMaker
import argparse
import json


class CurriculumMaker:

    def __init__(self, curriculum_type, n_files, n_arenas, time):
        self.curriculum_type = curriculum_type
        self.n_files = n_files
        self.path = f'../configs/curriculums/{curriculum_type}/'
        self.arena_maker = ArenaMaker(n_arenas, time)


    def makeArena(self):
        return self.arena_maker.make_arena(self.curriculum_type)


    def makeArenas(self):
        for n in range(self.n_files):
            arena = self.makeArena()
            file_name = f'{self.path}{self.curriculum_type}{n}.yaml'
            with open(file_name, 'w') as file:
                file.write(arena.makeYAML())
                print(f'Wrote arena to {file_name}')


    def makeCurriculum(self):
        self.makeArenas()

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
        for n in range(self.n_files):
            file_name = f'{self.curriculum_type}{n}.yaml'
            learner[CONFIG_FILES].append(file_name)
            if n > 0:
                learner[THRESHOLDS].append(n / self.n_files)

        file_name = f'{self.path}Learner.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(learner))
            print(f'Wrote Learner to {file_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Curriculum maker')
    parser.add_argument('-c', '--curriculum', help='Type of curriculum to make (y_maze, t_maze, radial_maze)')
    parser.add_argument('-n', '--num_arenas', help='Number of arenas per file.', type=int)
    parser.add_argument('-f', '--num_files', help='Number of files to make (curriculum will change this many times).', type=int)
    parser.add_argument('-t', '--time', help='Time limit of each arena.', type=int, default=500)

    args = parser.parse_args()

    curriculum = args.curriculum
    num_files = args.num_files
    num_arenas = args.num_arenas
    time = args.time

    curriculum_maker = CurriculumMaker(curriculum, num_files, num_arenas, time)

    curriculum_maker.makeCurriculum()
