# *********************************
# !!! WORKING GYM CODE WITH PPO !!!
# *********************************
import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

vec_envs = make_vec_env('CartPole-v1', n_envs=4)

model = PPO2(MlpPolicy, vec_envs, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo2_cartpole")

del model # remove to demonstrate saving and loading

model = PPO2.load("ppo2_cartpole")

# Enjoy trained agent
env = vec_envs.envs[0]
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
    if env.needs_reset:
        obs = env.reset()
env.env.close()