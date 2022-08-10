import gym
from gym import Env
from gym.spaces import Box, MultiDiscrete, Dict

import numpy as np

class CarEnv(Env):

    def __init__(self):
        pass
    
    def set_race(self, game):
        high = max(len(game.track), len(game.track[0])) * game.track[0][0].get_width()
        self.game = game
        self.action_space = MultiDiscrete([2, 3])
        self.factor = len(game.checkpoints) * game.max_laps
        self.observation_space = Box(0, 255, shape=(game.display_size[0], game.display_size[1], 3), dtype=np.uint8)
        # self.observation_space = Dict({"pos":Box(0, high, shape=(2,)), "angle":Box(low=0.0, high=360.0, shape=(1,)),"state":MultiDiscrete([len(game.checkpoints) + 1, game.max_laps + 1])})
        self.state = dict({"pos":np.array(game.car.get_pose()[0:2]).astype(np.float32), "angle":np.array(game.car.get_pose()[2:]).astype(np.float32), "state":np.array([0, game.max_laps]).astype(np.float32)})

    def step(self, action):
        lin = action[0]
        ang = action[1] - 1
        self.game.update(lin, ang)
        
        self.state = dict({"pos":np.array(self.game.car.get_pose()[0:2]).astype(np.float32), "angle":np.array(self.game.car.get_pose()[2:]).astype(np.float32), "state":np.array([self.game.checkpoint_counter, self.game.laps]).astype(np.integer)})

        curr_pos = self.game.checkpoints[self.state["state"][0]].copy()

        curr_pos[0] *= self.game.image_dimensions[0]
        curr_pos[0] += self.game.image_dimensions[0] / 2
        curr_pos[1] *= self.game.image_dimensions[1]
        curr_pos[1] += self.game.image_dimensions[1] / 2

        reward = -np.abs(self.state["pos"][0] - curr_pos[0]) - np.abs(self.state["pos"][1] - curr_pos[1]) - 128

        info = {}

        return self.game.get_picture(), reward, self.game.done, info


    def render(self, mode=None):
        self.game.draw()

    def reset(self):
        self.game.reset()
        self.game.randomize_start()
        self.set_race(self.game)
        return self.game.get_picture()