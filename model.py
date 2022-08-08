import gym
from gym import Env
from gym.spaces import Box, MultiDiscrete, Dict

class CarEnv(Env):

    def __init__(self):
        pass
    
    def set_race(self, game):
        high = max(len(game.track), len(game.track[0])) * game.track[0][0].get_width()
        self.game = game
        self.action_space = MultiDiscrete([2, 3])
        self.observation_space = Dict({"pos":Box(0, high, shape=(2,)), "angle":Box(0, 360, shape=(1,)),"state":MultiDiscrete([len(game.checkpoints), game.max_laps])})
        self.state = dict({"pos":game.car.get_pose()[0:2], "angle":game.car.get_pose()[2], "state":[0, game.max_laps]})

    def step(self, action):
        lin = action[0]
        ang = action[1] - 1
        reward = -0.1
        if self.game.update(lin, ang):
            reward += 1
        
        self.state = dict({"pos":self.game.car.get_pose()[0:2], "angle":self.game.car.get_pose()[2:], "state":[self.game.checkpoint_counter, self.game.laps]})

        info = {}

        return self.state, reward, self.game.done, info


    def render(self):
        self.game.draw()

    def reset(self):
        self.game.reset()
        self.set_race(self.game)
        return self.state