import random
import math
import pyglet
import entity
from pyglet.gl import *
import numpy
import simUI

config = pyglet.gl.Config(sample_buffer = 1, samples = 8)
window = pyglet.window.Window(1200, 1000, config = config)

# platform = pyglet.window.get_platform()
# display = platform.get_default_display()
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
# fps_display = pyglet.clock.ClockDisplay()

simPause = False
entities = []
population = []
popSize = 0
foodGroup = []
foodSize = 8
circleSize = 12
simSteps = 50
population2 = []


batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

batch2 = pyglet.graphics.Batch()

#Build circle vertex index list
def buildCircleIndex(inputList):
    outputList = []
    for i in range(1, inputList):
        outputList.append(0)
        outputList.append(i)
        outputList.append((i) % 12 + 1)
    return outputList


circleIndex = buildCircleIndex(circleSize + 1)


def spliceArray(array1, array2, mutationRate):
    if len(array1) != len(array2):
        raise ValueError('Array lengths not equal')
    outputArray = []
    originalShape = array1.shape

    fArray1 = array1.flatten()
    fArray2 = array2.flatten()

    for f in range(len(fArray1)):
        if random.random() > mutationRate:
            if random.random() > 0.5:
                outputArray.append(fArray1[f])
            else:
                outputArray.append(fArray2[f])
        else:
            outputArray.append((random.random() - .5) * 2)

    return numpy.array(outputArray).reshape(originalShape)

def reproduce():

    newCircle = entity.Circle(0, 500, 500, [66, 226, 244, 150])
    population.append(newCircle)
    newCircle.vertexList = batch.add_indexed(13, pyglet.gl.GL_TRIANGLES, None, circleIndex,
                                          ('v2f/stream', newCircle.computeVertex(12)),
                                          ('c4B/static', newCircle.buildColorVertex()))
    newCircle.lineToTarget = batch2.add(2, pyglet.gl.GL_LINES, None,
                                        ('v2f')
                                        )
    population2 = sorted(population, key=lambda x: x.score, reverse=True)
    # newCircle.nn.weights1 = population2[0].nn.weights1
    # newCircle.nn.weights2 = population2[0].nn.weights2
    parent1 = random.random
    newCircle.nn.weights1 = spliceArray(population2[0].nn.weights1, population2[1].nn.weights1, 0.15)
    newCircle.nn.weights2 = spliceArray(population2[0].nn.weights2, population2[1].nn.weights2, 0.15)


#Build all circle vertex points and store them as vertex lists in batch
def circleEntities(numPop):
    listOfCircles = []
    for i in range(numPop):
        newCircle = entity.Circle(i, 500, 500, [66, 226, 244, 150], batch)
        newCircle.vertexList = batch.add_indexed(13, pyglet.gl.GL_TRIANGLES, None, circleIndex,
                                             ('v2f/stream', newCircle.computeVertex(12)),
                                             ('c4B/static', newCircle.buildColorVertex()))
        newCircle.lineToTarget = batch2.add(2, pyglet.gl.GL_LINES, None,
                                    ('v2f')
                                    )

        listOfCircles.append(newCircle)
    return listOfCircles

def generateFood(numFood):
    for f in range(0, numFood):
        food = entity.Circle(f, random.randint(0, 1000), random.randint(0, 1000), [255, 255, 0, 255], batch)
        food.radius = 10
        foodGroup.append(food)
        food.vertexList = batch.add_indexed(13, pyglet.gl.GL_TRIANGLES, None, circleIndex,
                                              ('v2f/stream', food.computeVertex(12)),
                                              ('c4B/static', food.buildColorVertex()))

def findNearestFood(p):
    closestFood = entity.Circle
    nearestDistance = None
    ateFood = False
    for f in foodGroup:
        foodDist = p.distance((p.posX, p.posY), (f.posX, f.posY))
        if (foodDist < 35):
            f.delete()
            foodGroup.remove(f)
            p.score += 1
            p.hunger = 500
            ateFood = True
        elif nearestDistance == None or foodDist < nearestDistance:
            closestFood = f
            nearestDistance = foodDist
    p.targetFood = closestFood
    if ateFood:
        generateFood(1)


def removeDead():
    for to_remove in [i for i in population if not i.isActive]:
        to_remove.delete()
        to_remove.lineToTarget.delete()
        population.remove(to_remove)
        reproduce()

# class SimManager():
#     def __init__(self, populationList, foodList):
#         self.populationList = populationList
#         self.foodList = foodList

generateFood(foodSize)
population = circleEntities(32)
# uiElements = []

def update(dt):
    if not simPause:
        removeDead()
        for i in population:
            findNearestFood(i)
            i.update()
            i.statusTic()
        # for e in uiElements:
        #     e.update(dt)
        #     if e.timeCount <= 0:
        #         e.delete()
        #         uiElements.remove(e)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        global simPause
        simPause = not simPause
        print("Sim state toggled")

@window.event
def on_mouse_press(x, y, button, modifiers):
    for p in population:
        if p.distance((p.posX, p.posY), (x,y)) < 25:
            #newGUI = simUI.infoBox(p, batch2, foreground)
            #uiElements.append(newGUI)
            print(p.id)
    for f in foodGroup:
        if f.distance((f.posX, f.posY), (x,y)) < 10:
            print(f.id)
    pass

batch2.add(4, pyglet.gl.GL_QUADS, None,
                                    ('v2f', (1000, 0, 1200, 0, 1200, 1000, 1000, 1000)),
                                    ('c3B', (206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206, 206))
                                    )

pyglet.clock.schedule_interval(update, 1/60) # update at 60Hz

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    batch.draw()
    batch2.draw()
    # fps_display.draw()

pyglet.app.run()
