import math
import numpy as np

"""
Function to model car movement
"""
class Car:

    """
    Sets up the car with a given max velocity, acceleration, and angular velocity
    """
    def __init__(self, max_vel, acc, ang_vel, init_pose):
        self.max_vel = max_vel
        self.acc = acc
        self.ang_vel = ang_vel
        self.pose = init_pose
        self.vel = 0
    
    """
    Returns current pose of the car
    """
    def get_pose(self):
        return self.pose
    
    """
    Returns current velocity of the car
    """
    def get_vel(self):
        return self.vel
    
    """
    Updates the car position and velocity given inputs
    """
    def update(self, lin, ang):

        if lin != 0:
            self.vel += self.acc * lin
            if self.vel > self.max_vel:
                self.vel = self.max_vel
            elif self.vel < -self.max_vel:
                self.vel = -self.max_vel
        else:
            if self.vel > 0:
                self.vel = max(0, self.vel - self.acc)
            else:
                self.vel = min(0, self.vel + self.acc)

        ang = self.ang_vel * ang

        vel = self.vel

        if vel < 0:
            ang *= -1
        

        pose = np.zeros(3)
        pose[0] = self.pose[0] + vel * math.cos(self.pose[2] * math.pi / 180)
        pose[1] = self.pose[1] - vel * math.sin(self.pose[2] * math.pi / 180)
        pose[2] = self.pose[2] + ang
        pose[2] %= 360
        if pose[2] < 0:
            pose[2] += 360

        self.pose = tuple(pose)
    
    """
    Shifts the car to a given input and sets velocity to 0
    """
    def shift(self, x, y):
        self.vel = 0        
        pose = [0, 0, 0]
        pose[0] = self.pose[0] + x
        pose[1] = self.pose[1] + y
        pose[2] = self.pose[2]
        self.pose = tuple(pose)
    
    """
    Sets the car to a given pose and sets velocity to 0
    """
    def reset(self, pose):
        self.vel = 0
        self.pose = pose