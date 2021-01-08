import entity
import PythonNN
import pyglet
import math

class Agent(entity.Circle):
    def __init__(self, id, x, y, batch):
        colorCode = [66, 206, 244, 255]
        super().__init__(id, x, y, colorCode, batch)
        self.nn = PythonNN.NN()
        self.foodEaten = 0
        self.antennaPos = [(-25, 10), (25, 10)]
        self.antennaAngle = 90
        self.antennaLength = 50
        self.hunger = 500
        self.score = 0
        self.targetFood = None
        self.radius = 25

    def thinkMove(self, dt, targetPos):
        # self.nn.feedforward((self.distance(self.antennaPos[0],targetPos) / 1000,
        #                      self.distance(self.antennaPos[1], targetPos) / 1000,
        #                      self.distance((self.posX, self.posY),targetPos) / 1000,
        #                      self.rot / 360))
        self.nn.feedforward((self.distance((self.antennaLength * math.cos(math.radians(self.rot - self.antennaAngle/2)) + self.posX,
                                            self.antennaLength * math.sin(math.radians(self.rot - self.antennaAngle/2)) + self.posY),
                                           targetPos) / 750,
                             self.distance((self.antennaLength * math.cos(math.radians(self.rot + self.antennaAngle / 2)) + self.posX,
                                            self.antennaLength * math.sin(math.radians(self.rot + self.antennaAngle / 2)) + self.posY),
                                           targetPos) / 750,
                             self.distance((self.posX, self.posY), targetPos) / 750))
        self.nnMove(self.nn.output[0], self.nn.output[1], dt)

    def findNearestFood(self, foodList):
        if len(foodList) is not 0:
            closestFood = foodList[0]
            nearestDistance = self.distance((self.posX, self.posY), (foodList[0].posX, foodList[0].posY))
            for f in foodList:
                dist = self.distance((self.posX, self.posY), (f.posX, f.posY))
                if dist < 35 and f.isActive:
                    f.isActive = False
                    self.score += 1
                    self.hunger = 500
                elif dist < nearestDistance:
                    closestFood = f
                    nearestDistance = dist
            self.targetFood = closestFood
        else:
            self.targetFood = None

    def statusTic(self):
        self.hunger += -1
        if self.hunger <= 0 and self.isActive:
            self.isActive = False

    def update(self, dt, foodGroup):
        if self.isActive:
            self.findNearestFood(foodGroup)
            #self.lineToTarget.vertices = [self.posX, self.posY, self.targetFood.posX, self.targetFood.posY]
            self.ant.vertices = [self.antennaLength * math.cos(math.radians(self.rot - self.antennaAngle/2)) + self.posX,
                                 self.antennaLength * math.sin(math.radians(self.rot - self.antennaAngle/2)) + self.posY,
                                 self.posX, self.posY, self.posX, self.posY,
                                 self.antennaLength * math.cos(math.radians(self.rot + self.antennaAngle / 2)) + self.posX,
                                 self.antennaLength * math.sin(math.radians(self.rot + self.antennaAngle / 2)) + self.posY
                                 ]
            if self.targetFood is not None:
                self.thinkMove(dt, (self.targetFood.posX, self.targetFood.posY))
            #self.vertexList.vertices = self.computeVertex(12)
            #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            #                      ('v2f', (self.posY, self.posY, self.antennaPos[0][0], self.antennaPos[0][1]))
            #                      )
            self.statusTic()
            self.vertexList.vertices = self.computeVertex(12)
            super().update()