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
        pose = [0, 0, 0]
        pose[0] = self.pose[0] - self.vel * math.cos(self.pose[2] * math.pi / 180)
        pose[1] = self.pose[1] + self.vel * math.sin(self.pose[2] * math.pi / 180)
        pose[2] = self.pose[2] - ang
        pose[2] %= 360
        if pose[2] < 0:
            pose[2] += 360

        self.pose = tuple(pose)
        print(self.pose)