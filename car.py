import math

class Car:

    def __init__(self, max_vel, acc, ang_vel, init_pose):
        self.max_vel = max_vel
        self.acc = acc
        self.ang_vel = ang_vel
        self.pose = init_pose
        self.vel = 0
    
    def get_pose(self):
        return self.pose
    
    def get_vel(self):
        return self.vel
    
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
        

        pose = [0, 0, 0]
        pose[0] = self.pose[0] + vel * math.cos(self.pose[2] * math.pi / 180)
        pose[1] = self.pose[1] - vel * math.sin(self.pose[2] * math.pi / 180)
        pose[2] = self.pose[2] + ang
        pose[2] %= 360
        if pose[2] < 0:
            pose[2] += 360

        self.pose = tuple(pose)
        # print(self.pose)
    
    def shift(self, x, y):
        self.vel = 0        
        pose = [0, 0, 0]
        pose[0] = self.pose[0] + x
        pose[1] = self.pose[1] + y
        pose[2] = self.pose[2]
        self.pose = tuple(pose)
    
    def reset(self, pose):
        self.vel = 0
        self.pose = pose