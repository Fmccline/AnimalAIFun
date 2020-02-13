import gym

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import make_vec_env
from stable_baselines import DQN, PPO2
import random
import argparse

# Constants
ENV_PATH = '../env/AnimalAI'
WORKER_ID = random.randint(1, 100)
SUPPORTED_MODELS = {'dqn': DQN, 'ppo': PPO2}

# Parser
parser = argparse.ArgumentParser(description='AnimalAI Agent Trainer')

# Required
parser.add_argument('-m', '--model', help=f'Model to use {SUPPORTED_MODELS}')

# Optional
parser.add_argument('-l', '--load_path', help='The file name to load the model from. Training will not happen', default=None)
parser.add_argument('-s', '--save_path', help='The file name to save the model to', default=None)
parser.add_argument('-a', '--arena_config', help='The path to the arena YAML config', default='configs/1-Food.yaml')
parser.add_argument('-t', '--total_timesteps', help='The total time steps for training', type=int, default=10000)
parser.add_argument('-v', '--verbose', help='Whether training should be verbose', type=int, default=0)

args = parser.parse_args()

    
def create_env_fn():
    env = AnimalAIEnv(environment_filename=ENV_PATH,
                    worker_id=WORKER_ID,
                    n_arenas=1,
                    arenas_configurations=ArenaConfig(args.arena_config),
                    docker_training=False,
                    retro=True)
    return env

def create_model(env):
    modelType = args.model
    if modelType not in SUPPORTED_MODELS.keys():
        raise ValueError(f'Model type {modelType} is not supported. Use a model in this list: {SUPPORTED_MODELS.keys()}')

    if args.load_path is not None:
        model = SUPPORTED_MODELS[modelType].load(args.load_path)
    elif args.save_path is not None:
        model = SUPPORTED_MODELS[modelType]('MlpPolicy', env, verbose=args.verbose)
    else:
        raise ValueError(f'Must provide a model to load from or save to with "-l" or "-s"')
    return model

if __name__ == '__main__':

    env = make_vec_env(create_env_fn, n_envs=1)
    model = create_model(env)

    if args.save_path is not None:
        print('\nTraining model now\n')
        model.learn(total_timesteps=args.total_timesteps)
        print('\n\n\n\nDone learning!\n\n\n\n')
        model.save(args.save_path)
    elif args.load_path is not None:
        print("Demonstrating model. Press CTRL-C to exit")
        obs = env.reset()
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
