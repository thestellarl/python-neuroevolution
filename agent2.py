import entity
import PythonNN

class Agent2(entity.Circle):
    def __init__(self, id, x, y, batch):
        colorCode = [220, 140, 140, 255]
        super().__init__(id, x, y, colorCode, batch)
        foodVal = 1
        self.radius = 25
        self.nn = PythonNN.NN()
        self.score = 0
        self.foodEaten = 0
        self.antennaPos = [(-25, 10), (25, 10)]
        self.hunger = 500;
        print("Agent 2 created")

    def thinkMove(self, dt, targetPos):
        self.nn.feedforward((self.distance(self.antennaPos[0],targetPos) / 1000,
                             self.distance(self.antennaPos[1], targetPos) / 1000,
                             self.distance((self.posX, self.posY),targetPos) / 1000,
                             self.rot / 360))
        self.nnMove(self.nn.output[0], self.nn.output[1], dt)

    def findNearestFood(self, foodList):
        if len(foodList) is not 0:
            closestFood = foodList[0]
            nearestDistance = self.distance((self.posX, self.posY), (foodList[0].posX, foodList[0].posY))
            for f in foodList[1:]:
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

    def update(self, dt, foodGroup):
        self.findNearestFood(foodGroup)
        self.lineToTarget.vertices = [self.posX, self.posY, self.targetFood.posX, self.targetFood.posY]
        self.thinkMove(dt, (self.targetFood.posX, self.targetFood.posY))
        #self.vertexList.vertices = self.computeVertex(12)
        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #                      ('v2f', (self.posY, self.posY, self.antennaPos[0][0], self.antennaPos[0][1]))
        #                      )
        #self.statusTic()
        super().update()