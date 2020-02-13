import gym

from animalai.envs.gym.environment import AnimalAIEnv
from animalai.envs.arena_config import ArenaConfig
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
import random

env_path = '../env/AnimalAI'
worker_id = random.randint(1, 100)
arena_config_in = ArenaConfig('configs/1-Food.yaml')

def create_env_fn():
    env = AnimalAIEnv(environment_filename=env_path,
                      worker_id=worker_id,
                      n_arenas=1,
                      arenas_configurations=arena_config_in,
                      docker_training=False,
                      retro=True)
    return env


env = make_vec_env(create_env_fn, n_envs=1)

model = PPO2(MlpPolicy, env, verbose=0)
model.learn(total_timesteps=int(1e6))
print('\n\n\n\nDone learning!\n\n\n\n')
model.save("ppo_v0.0")

#model = PPO2.load('my_ppo_test')

obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
