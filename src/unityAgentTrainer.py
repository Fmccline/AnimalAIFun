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
        self.number_arenas = 1 if watch else num_agents

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
        tc.start_learning(env, self.trainer_config)
