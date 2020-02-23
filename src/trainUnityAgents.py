from animalai_train.trainers.trainer_controller import TrainerController
from animalai.envs import UnityEnvironment
from animalai.envs.exception import UnityEnvironmentException
from animalai.envs.arena_config import ArenaConfig
from animalai_train.trainers.meta_curriculum import MetaCurriculum
import random
import yaml
import sys
import argparse
import datetime


class UnityAgentTrainer:

    ENV_PATH = '../env/AnimalAI'
    WORKER_ID = random.randint(1, 100)
    SEED = 10
    BASE_PORT = 5005
    SUB_ID = 1
    SAVE_FREQ = 5000
    KEEP_CHECKPOINTS = 5000
    LESSON = 0
    RUN_SEED = 1
    DOCKER_TARGET_NAME = None
    SUMMARIES_DIR = './summaries'

    def __init__(self, run_id, trainer_config_path, arena_config_path, num_agents, new_model=False, watch=False, curriculum_type=None):
        self.run_id = run_id

        self.trainer_config = self.load_config(trainer_config_path)
        self.arena_config = ArenaConfig(arena_config_path)

        self.load_model = not new_model
        self.watch = watch
        self.number_arenas = 1 if watch_ai else num_agents

        self.maybe_meta_curriculum = None if curriculum_type is None else MetaCurriculum(f'./configs/curriculums/{curriculum_type}/')
        self.model_path = f'./models/{run_id}'


    def load_config(self, trainer_config_path):
        try:
            with open(trainer_config_path) as data_file:
                trainer_config = yaml.load(data_file)
                return trainer_config
        except IOError:
            raise UnityEnvironmentException('Parameter file could not be found '
                                            'at {}.'
                                            .format(trainer_config_path))
        except UnicodeDecodeError:
            raise UnityEnvironmentException('There was an error decoding '
                                            'Trainer Config from this path : {}'
                                            .format(trainer_config_path))


    def init_environment(self):
        docker_training = self.DOCKER_TARGET_NAME is not None
        env_path = (self.ENV_PATH.strip()
                        .replace('.app', '')
                        .replace('.exe', '')
                        .replace('.x86_64', '')
                        .replace('.x86', ''))

        return UnityEnvironment(
            n_arenas=self.number_arenas, # Change this to train on more arenas
            file_name=env_path,
            worker_id=self.WORKER_ID,
            seed=self.SEED,
            docker_training=docker_training,
            play=False,
            inference=self.watch # True to watch agent play
        )

    def train(self):
        env = self.init_environment()

        external_brains = {}
        for brain_name in env.external_brain_names:
            external_brains[brain_name] = env.brains[brain_name]

        # Create controller and begin training.
        tc = TrainerController(self.model_path, self.SUMMARIES_DIR, self.run_id + '-' + str(self.SUB_ID),
                            self.SAVE_FREQ, self.maybe_meta_curriculum,
                            self.load_model, not self.watch,
                            self.KEEP_CHECKPOINTS, self.LESSON, external_brains, self.RUN_SEED, self.arena_config)
        start = datetime.datetime.now()
        tc.start_learning(env, self.trainer_config)
        end = datetime.datetime.now()
        total_time = end - start
        print(f'Finished training after {round(total_time.seconds / 60 / 60, 3)} hours.')


parser = argparse.ArgumentParser(description='Trainer for Unity ML Agents with the AnimalAI environment')
parser.add_argument('-f', '--model_name', dest='model_name', help='Name of model to train.')
parser.add_argument('-t', '--trainer_path', dest='trainer_path', default='configs/trainers/default_trainer.yaml', help='Optional path to trainer config to use.')
parser.add_argument('-c', '--curriculum', dest='curriculum', default=None, help='Optional name of curriculum to train from')
parser.add_argument('-a', '--arena_config', dest='arena_config', default=None, help='Path to arena config')
parser.add_argument('-d', '--num_agents', dest='num_agents', default=None, help='Optional name of curriculum to train from', type=int)
parser.add_argument('-w', '--watch', dest='watch_ai', default=False, action='store_true', help='Boolean for whether user wants to watch the AI or not.')
parser.add_argument('-n', '--new_model', dest='new_model', default=False, action='store_true', help='Boolean for whether to create a new model or load from an existing model.')

if __name__ == '__main__':
    args = parser.parse_args()

    model_name = args.model_name
    trainer_path = args.trainer_path
    curriculum_type = args.curriculum
    arena_config = 'configs/arenas/baseline_arena.yaml' if args.arena_config is None else args.arena_config
    num_agents = args.num_agents
    watch_ai = args.watch_ai 
    if args.new_model:
        do_it = input('Are you sure you want to create a new model? (y/n)\n')
        new_model = True if do_it == 'y' or do_it == 'Y' else False
    else:
        new_model = False

    trainer = UnityAgentTrainer(model_name, trainer_path, arena_config, num_agents, new_model, watch_ai, curriculum_type)
    trainer.train()
