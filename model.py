import gym
from gym import env
from gym.spaces import Discrete, Box

import numpy as np

from stable_baselines3 import PPO

class CarEnv(Env):

    def __init__(self):
        pass
    
    def set_race(self, track, checkpoints, start_pos):
        self.track = track
        self.checkpoints = checkpoints
        self.start_pos = start_pos
        self.action_space = MultiDiscrete([3, 3])
        self.observation_space = tuple(Box(3,), Discrete(len(checkpoints)))

    def step(self, action):
        pass

    def render(self):
        pass

    def reset(self):
        self.state = tuple(self.start_pos, 0)