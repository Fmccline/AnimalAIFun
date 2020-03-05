from dumbAgent import DumbAgent

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


class DumbAgentRunner:

    ENV_PATH = '../env/AnimalAI'
    WORKER_ID = random.randint(1, 100)
    SEED = 10

    def __init__(self, arena_config_path, num_agents, watch=False):
        self.arena_config = ArenaConfig(arena_config_path)
        self.watch = watch
        self.number_arenas = 1 if watch else num_agents


    def init_environment(self):
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
            arenas_configurations=self.arena_config,
            inference=self.watch # True to watch agent play
        )

    def run(self):
        dumbAgent = DumbAgent()
        env = self.init_environment()

        actions = [0,0]
        env.reset(arenas_configurations = self.arena_config)
        print("Enter CTRL-C to exit program.")
        try:
            while True:
                info = env.step(vector_action=actions)
                brain = info['Learner']
                pixels = brain.visual_observations    # list of n_arenas pixel observations, each of size (84x84x3)
                speeds = brain.vector_observations    # list of n_arenas speeds, each of size 3
                rewards = brain.rewards               # list of n_arenas float rewards
                is_done = brain.local_done            # list of n_arenas booleans to flag if each agent is done or not
                actions = dumbAgent.step(pixels, rewards, is_done, info)
        except KeyboardInterrupt:
            print("\nExiting progam.")
        finally:
            env.close()


if __name__ == '__main__':
    arena_path = '/configs/arenas/baseline_arena.yaml'
    num_agents = 1
    runner = DumbAgentRunner(arena_path, num_agents, watch=True)
    runner.run()