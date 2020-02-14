import gym

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import make_vec_env
from stable_baselines import DQN, PPO2
import random
import argparse
import datetime

# Constants
ENV_PATH = '../env/AnimalAI'
WORKER_ID = random.randint(1, 100)
SUPPORTED_MODELS = {'dqn': DQN, 'ppo': PPO2}

# Parser
parser = argparse.ArgumentParser(description='AnimalAI Agent Trainer')

# Required
parser.add_argument('-m', '--model', help=f'Model to use {SUPPORTED_MODELS}')
parser.add_argument('-f', '--model_path', help=f'The file path to the model')

# Optional
parser.add_argument('-i', '--inference', help='Falg to watch model instead of train. Boolean value {0,1}', type=int, default=0)
parser.add_argument('-a', '--arena_config', help='The path to the arena YAML config', default='configs/base_test.yaml')
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

def get_model():
    modelType = args.model
    if modelType not in SUPPORTED_MODELS.keys():
        raise ValueError(f'Model type {modelType} is not supported. Use a model in this list: {SUPPORTED_MODELS.keys()}')
    model = SUPPORTED_MODELS[modelType]
    return model


if __name__ == '__main__':
    env = make_vec_env(create_env_fn, n_envs=1)
    modelType = get_model()
    modelPath = args.model_path
    if args.inference != 0:
        model = modelType.load(modelPath)
        print("Demonstrating model. Press CTRL-C to exit.")
        obs = env.reset()
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
    else:
        model = modelType('MlpPolicy', env, verbose=args.verbose)
        start = datetime.datetime.now()
        print(f'\nTraining model now at {start}\n')
        try:
            model.learn(total_timesteps=args.total_timesteps)
            print('Done training!')
        except KeyboardInterrupt:
            print('\nKeyboard Interrupt. Saving model then exiting program.')
        finally:
            end = datetime.datetime.now()
            model.save(modelPath)
            print(f'Trained for {round((end - start).seconds / 60 / 60, 2)} hours.\nSaved model to {modelPath}')
