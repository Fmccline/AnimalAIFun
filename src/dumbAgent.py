import numpy as np


class Colors:
    GREENS = 'Greens'
    YELLOWS = 'Yellows'
    REDS = 'Reds'
    GREEN_ARR = np.array([129,191,65], np.int32)
    YELLOW_ARR = np.array([100, 65, 5], np.int32)
    RED_ARR = np.array([185,50,50], np.int32)


class DumbAgent(object):

    def __init__(self):
        """
         Load your agent here and initialize anything needed
         WARNING: any path to files you wish to access on the docker should be ABSOLUTE PATHS
        """
        self.last_turn = 1
        self.prev_obs = {Colors.GREENS: 0, Colors.YELLOWS: 0, Colors.REDS: 0}
        self.speed_limit = 8

    def reset(self, t=250):
        """
        Reset is called before each episode begins
        Leave blank if nothing needs to happen there
        :param t the number of timesteps in the episode
        """

    def step(self, obs, reward, done, info):
        """
        A single step the agent should take based on the current state of the environment
        We will run the Gym environment (AnimalAIEnv) and pass the arguments returned by env.step() to
        the agent.

        Note that should if you prefer using the BrainInfo object that is usually returned by the Unity
        environment, it can be accessed from info['brain_info'].

        :param obs: agent's observation of the current environment
        :param reward: amount of reward returned after previous action
        :param done: whether the episode has ended.
        :param info: contains auxiliary diagnostic information, including BrainInfo.
        :return: the action to take, a list or size 2
        """
        brain = info['Learner']

        pixels = brain.visual_observations  # list of n_arenas pixel observations, each of size (84x84x3)
        speeds = brain.vector_observations  # list of n_arenas speeds, each of size 3
        rewards = brain.rewards             # list of n_arenas float rewards
        is_done = brain.local_done          # list of n_arenas booleans to flag if each agent is done or not
        
        for pixel in np.nditer(pixels, op_flags=['readwrite']):
            pixel[...] = pixel*255

        turn_action = self.get_turn_action(pixels)
        accel_action = self.get_accel_action(speeds)

        actions = [accel_action, turn_action]
        return actions

    def get_turn_action(self, pixels):
        action = self.last_turn
        g_colors = self.get_colours(pixels, Colors.GREEN_ARR)
        y_colors =  self.get_colours(pixels, Colors.YELLOW_ARR)
        r_colors = self.get_colours(pixels, Colors.RED_ARR)
        # go the other way if we should
        if y_colors < self.prev_obs[Colors.YELLOWS]:
            action = self.turn_other_way(action)
        elif g_colors < self.prev_obs[Colors.GREENS]:
            action = self.turn_other_way(action)
        elif r_colors > self.prev_obs[Colors.REDS]:
            action = self.turn_other_way(action)

        self.prev_obs[Colors.YELLOWS] = y_colors
        self.prev_obs[Colors.GREENS] = g_colors
        self.prev_obs[Colors.REDS] = r_colors
        self.last_turn = action
        return action

    def turn_other_way(self, current_turn):
        return 1 if current_turn == 2 else 2

    def get_accel_action(self, speeds):
        speed = np.linalg.norm(speeds)
        if speed > self.speed_limit:
            return 0
        else:
            return 1

    @staticmethod
    def get_colours(pixels, color):
        min_threshold = np.all(pixels > np.minimum(color*0.8, color-25), axis=-1)
        max_threshold = np.all(pixels < np.maximum(color*1.2, color+25), axis=-1)
        return np.count_nonzero((min_threshold & max_threshold) == True)


