import pyglet
import math
import random

class PhysicalObject(object):
    def __init__(self, id, x = None, y = None):
        self.posX, self.posY = x, y
        self.velocity_x, self.velocity_y = random.random() * 10 - 5,random.random() * 10 - 5
        self.speed = 25
        self.rot = random.randint(0, 359)
        self.id = id


    def distance(self, point_1=(0, 0), point_2=(0, 0)):
        return math.sqrt(
            (point_1[0] - point_2[0]) ** 2 +
            (point_1[1] - point_2[1]) ** 2)
    def nnMove(self, v, angularVelocity, dt):
        self.rot += (angularVelocity - 0.5) * 80
        #if self.posX * (v * 200) + math.cos(math.radians(self.rot)) > 0 and self.posX + math.cos(math.radians(self.rot)) < 1000:
        self.posX += math.cos(math.radians(self.rot)) * (v * 200) * dt
        #if self.posY * (v * 200) + math.cos(math.radians(self.rot)) > 0 and self.posY + math.cos(math.radians(self.rot)) < 1000:
        self.posY += math.sin(math.radians(self.rot)) * (v * 200) * dt
    def update(self):
        pass
        #self.rot = self.rot % 360