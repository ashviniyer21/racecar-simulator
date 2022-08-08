import pygame as pg
from car import Car
from model import CarEnv
import os
import numpy as np
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


class Game:
    def __init__(self, track, start, laps, fps, car):
        self.track = track
        self.track_mask = []
        self.get_mask()
        self.checkpoints = []
        pos = start[0:2]
        dir = start[2]
        pos = self.get_next(pos, dir)
        self.get_checkpoints(pos, dir)
        self.max_laps = laps
        self.laps = laps
        self.checkpoint_counter = 0
        self.FINISH_LINE = pg.image.load("images/finishline.png")

        self.window = pg.display.set_mode((500, 500), pg.RESIZABLE)
        pg.display.set_caption("Racecar Simulator")
        pg.init()

        self.font = pg.font.Font(pg.font.get_default_font(), 12)
        self.text = self.font.render("Laps left: " + str(laps), True, pg.Color(0, 0, 0, 1))
        self.clock = pg.time.Clock()
        self.fps = fps
        self.car = car

        self.finishlineloc = [0, 0]
        self.get_finish_line()
        self.done = False
        self.update(0, 0)
    
    def get_finish_line(self):

        finish1 = self.checkpoints[0]
        finish2 = self.checkpoints[len(self.checkpoints) - 2]
        if finish1[0] == finish2[0]:
            self.finishlineloc[0] = finish1[0] * IMAGE_WIDTH + 16
            self.finishlineloc[1] = max(finish1[1], finish2[1]) * IMAGE_HEIGHT - 8
        else:
            self.finishlineloc[1] = finish1[1] * IMAGE_HEIGHT + 16
            self.finishlineloc[0] = max(finish1[0], finish2[0]) * IMAGE_HEIGHT - 8
            self.FINISH_LINE = pg.transform.rotate(self.FINISH_LINE, 90)
    
    def get_checkpoints(self, pos, dir):
        while pos[0] != start[0] or pos[1] != start[1]:
            self.checkpoints.append(pos)
            if self.track[pos[1]][pos[0]] == TOP_LEFT:
                if(dir == 90):
                    dir = 0
                else:
                    dir = 270
            if self.track[pos[1]][pos[0]] == TOP_RIGHT:
                if(dir == 90):
                    dir = 180
                else:
                    dir = 270
            if self.track[pos[1]][pos[0]] == BOTTOM_LEFT:
                if(dir == 270):
                    dir = 0
                else:
                    dir = 90
            if self.track[pos[1]][pos[0]] == BOTTOM_RIGHT:
                if(dir == 270):
                    dir = 180
                else:
                    dir = 90
            pos = self.get_next(pos, dir)

        self.checkpoints.append(pos)
        self.checkpoints.append(self.checkpoints[0])

    def get_mask(self):
         for i in range(len(self.track)):
            row = []
            for j in range(len(self.track[i])):
                if self.track[i][j] == TOP_LEFT:
                    row.append(TOP_LEFT_MASK)
                elif self.track[i][j] == TOP_RIGHT:
                    row.append(TOP_RIGHT_MASK)
                elif self.track[i][j] == BOTTOM_LEFT:
                    row.append(BOTTOM_LEFT_MASK)
                elif self.track[i][j] == BOTTOM_RIGHT:
                    row.append(BOTTOM_RIGHT_MASK)
                elif self.track[i][j] == HORIZONTAL:
                    row.append(HORIZONTAL_MASK)
                elif self.track[i][j] == VERTICAL:
                    row.append(VERTICAL_MASK)
                else:
                    row.append(None)
            self.track_mask.append(row)
    
    def get_next(self, pos, dir):
        new = [pos[0], pos[1]]
        if dir == 0:
            new[0] += 1
        elif dir == 90:
            new[1] -= 1
        elif dir == 180:
            new[0] -= 1
        else:
            new[1] += 1
        return new
    
    def check_collision(self, pose, rotated_car, new_rect):
        gridx = int(pose[0] // IMAGE_WIDTH)
        gridy = int(pose[1] // IMAGE_HEIGHT)
        car_mask = pg.mask.from_surface(rotated_car)
        for i in range(gridx, gridx + 2):
            for j in range(gridy, gridy + 2):
                if i == len(track[0]) or j == len(track) or self.track_mask[j][i] == None:
                    continue
                offset = (new_rect.topleft[0] - i * IMAGE_WIDTH, new_rect.topleft[1] - j * IMAGE_HEIGHT)
                temp = self.track_mask[j][i].overlap(car_mask, offset)
                if temp != None:
                    return temp
        return None

    def update(self, lin, ang):

        if self.done:
            lin = 0
            ang = 0

        self.clock.tick(self.fps)
        self.car.update(lin, ang)
        pose = self.car.get_pose()
        rotated_car = pg.transform.rotate(CAR, pose[2])

        new_rect = rotated_car.get_rect(
            center=CAR.get_rect(topleft=pose[0:2]).center)

        collision = self.check_collision(pose, rotated_car, new_rect)

        while collision != None:
            xshift = 0
            yshift = 0
            if(collision[0] < 20):
                xshift = 1
            elif(collision[0] > 100):
                xshift = -1
            if(collision[1] < 20):
                yshift = 1
            elif(collision[1] > 100):
                yshift = -1
            car.shift(xshift, yshift)
            pose = car.get_pose()
            rotated_car = pg.transform.rotate(CAR, pose[2])
            new_rect = rotated_car.get_rect(
                center=CAR.get_rect(topleft=pose[0:2]).center)
            collision = self.check_collision(pose, rotated_car, new_rect)
        
        gridx = int(pose[0] // IMAGE_WIDTH)
        gridy = int(pose[1] // IMAGE_HEIGHT)

        checkpoint = False

        if self.checkpoints[self.checkpoint_counter][0] == gridx and self.checkpoints[self.checkpoint_counter][1] == gridy:
            self.checkpoint_counter += 1
            checkpoint = True
            if self.checkpoint_counter == len(self.checkpoints):
                self.checkpoint_counter = 0
                self.laps -= 1
                self.text = self.font.render("Laps left: " + str(self.laps), True, pg.Color(0, 0, 0, 1))
                if self.laps == 0:
                    print("You won!")
                    self.done = True
        
        self.pose = pose
        self.rotated_car = rotated_car
        self.new_rect = new_rect
        
        return checkpoint

    
    def draw(self):
        pose = self.pose
        rotated_car = self.rotated_car
        new_rect = self.new_rect
        center = self.window.get_rect().center

        offset = (-pose[0] + center[0], -pose[1] + center[1])

        self.window.fill((0, 192, 0))

        for i in range(len(self.track)):
            for j in range(len(self.track[i])):
                self.window.blit(self.track[i][j], (j * IMAGE_WIDTH + offset[0], i * IMAGE_HEIGHT + offset[1]))

        self.window.blit(self.FINISH_LINE, (self.finishlineloc[0] + offset[0], self.finishlineloc[1] + offset[1]))
        
        self.window.blit(rotated_car, (new_rect.topleft[0] + offset[0], new_rect.topleft[1] + offset[1]))

        self.window.blit(self.text, (16, 16))

        pg.display.update()

    
    def reset(self):
        self.car.reset([IMAGE_WIDTH / 4 + start[0] * IMAGE_WIDTH, IMAGE_HEIGHT / 4 + start[1] * IMAGE_HEIGHT, start[2]])
        self.done = False
        self.laps = self.max_laps
        self.checkpoint_counter = 0
        self.text = self.font.render("Laps left: " + str(self.laps), True, pg.Color(0, 0, 0, 1))

HORIZONTAL = pg.image.load("images/horizontal.png")
VERTICAL = pg.image.load("images/vertical.png")
TOP_LEFT = pg.image.load("images/topleft.png")
TOP_RIGHT = pg.image.load("images/topright.png")
BOTTOM_LEFT = pg.image.load("images/bottomleft.png")
BOTTOM_RIGHT = pg.image.load("images/bottomright.png")

HORIZONTAL_MASK = pg.mask.from_surface(pg.image.load("images/horizontalmask.png"))
VERTICAL_MASK = pg.mask.from_surface(pg.image.load("images/verticalmask.png"))
TOP_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/topleftmask.png"))
TOP_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/toprightmask.png"))
BOTTOM_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/bottomleftmask.png"))
BOTTOM_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/bottomrightmask.png"))

GRASS = pg.image.load("images/grass.png")
CAR = pg.transform.scale(pg.image.load("images/car.png"), (60, 48))

track = [
    [TOP_LEFT, HORIZONTAL, HORIZONTAL, TOP_RIGHT],
    [VERTICAL, GRASS, GRASS, VERTICAL],
    [BOTTOM_LEFT, HORIZONTAL, HORIZONTAL, BOTTOM_RIGHT]
    ]

start = [0, 0, 0] #Grid space, angle for starting driving

IMAGE_WIDTH, IMAGE_HEIGHT = HORIZONTAL.get_width(), HORIZONTAL.get_height()

MAX_LAPS = 3

FPS = 60

car = Car(5, 0.05, 3, np.array([IMAGE_WIDTH / 4 + start[0] * IMAGE_WIDTH, IMAGE_HEIGHT / 4 + start[1] * IMAGE_HEIGHT, start[2]]))

game = Game(track, start, MAX_LAPS, FPS, car)

def auto():

    env = CarEnv()
    env.set_race(game)
    print(env.observation_space.sample())
    # print(env.action_space.sample())

    # episodes = 5
    # for episode in range(1, episodes+1):
    #     state = env.reset()
    #     done = False
    #     score = 0 
        
    #     while not done:
    #         env.render()
    #         action = env.action_space.sample()
    #         n_state, reward, done, info = env.step(action)
    #         score+=reward
    #     print('Episode:{} Score:{}'.format(episode, score))
    # env.close()
    check_env(env)

    log_path = os.path.join('Training', 'Logs')
    model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)
    model.learn(total_timesteps=1000)


def manual():

    run = True

    lin = 0
    ang = 0

    while run:

        for event in pg.event.get():
            if event == pg.QUIT:
                run = False
                break

        keys = pg.key.get_pressed()

        lin = 0
        ang = 0

        if keys[pg.K_SPACE]:
            game.reset()

        if keys[pg.K_w]:
            lin += 1
        if keys[pg.K_s]:
            lin -= 1
        if keys[pg.K_a]:
            ang += 1
        if keys[pg.K_d]:
            ang -= 1

        game.update(lin, ang)
        game.draw()

    pg.quit()

manual()