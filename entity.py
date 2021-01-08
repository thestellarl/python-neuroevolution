import pyglet
import numpy
import math
import physicalobject
import PythonNN

class Circle(physicalobject.PhysicalObject):

    def __init__(self, id, x, y, colorCode, batch):
        super().__init__(id, x, y)
        # self.nn = PythonNN.NN()
        self.radius = 10
        self.colorVerts = colorCode
        #self.vertexList = pyglet.graphics.vertex_list(13, 'v2f')
        self.vertexList = batch.add_indexed(13, pyglet.gl.GL_TRIANGLE_STRIP, None, self.buildCircleIndex(13), 'v2f', 'c4B/static')
        self.vertexList.vertices = self.computeVertex(12)
        self.vertexList.colors = self.buildColorVertex()
        #self.lineToTarget = pyglet.graphics.vertex_list(2, 'v2f')
        self.lineToTarget = batch.add(2, pyglet.gl.GL_LINES, None, 'v2f')
        self.ant = batch.add(4, pyglet.gl.GL_LINES, None, 'v2f')
        self.isActive = True

    def delete(self):
        self.vertexList.delete()
        self.lineToTarget.delete()
        self.ant.delete()

    def setColor(self):
        pass

    def buildColorVertex(self):
        while self.vertexList.get_size() * 4 > len(self.colorVerts):
            self.colorVerts += self.colorVerts[0:4]
        return self.colorVerts

    # Build circle vertex index list
    def buildCircleIndex(self, cVertexNum):
        outputList = [0, 0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 7, 0, 7, 8, 0, 8, 9, 0, 9, 10, 0, 10, 11, 0, 11, 12, 0, 1, 12, 12]
        # for i in range(1, cVertexNum - 1):
        #     outputList.append(0)
        #     outputList.append((i) % 11 + 1)
        #     outputList.append((i) % 12 + 1)
        # print(outputList)
        return outputList

    def computeVertex(self, points):
        circle_vertex = []
        circle_vertex.append(self.posX)
        circle_vertex.append(self.posY)
        for deg in range(0, 360, int(360 / points)):
            circle_vertex.append(int(math.cos(math.radians(deg + self.rot)) * self.radius + self.posX))
            circle_vertex.append(int(math.sin(math.radians(deg + self.rot)) * self.radius + self.posY))
        return circle_vertex

    # def statusTic(self):
    #     self.hunger += -1
    #     if self.hunger <= 0 and self.alive:
    #         self.alive = False

    # def findNearestFood(self, foodList):
    #     closestFood = Circle
    #     nearestDistance = None
    #     ateFood = False
    #     for f in foodList:
    #         foodDist = self.distance((self.posX, self.posY), (f.posX, f.posY))
    #         if (foodDist < 35):
    #             f.alive = False
    #             self.score += 1
    #             self.hunger = 500
    #         elif nearestDistance == None or foodDist < nearestDistance:
    #             closestFood = f
    #             nearestDistance = foodDist
    #     self.targetFood = closestFood

    def update(self):
        super().update()
        pass
        #self.findNearestFood(foodGroup)
        #self.thinkMove(dt, (self.targetFood.posX, self.targetFood.posY))
        #print(self.id)
        #self.vertexList.vertices = self.computeVertex(12)
        #pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #                      ('v2f', (self.posY, self.posY, self.antennaPos[0][0], self.antennaPos[0][1]))
        #                      )
        #self.statusTic()
