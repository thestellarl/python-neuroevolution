import random
import math
import pyglet
import entity
import agent
import agent2
import food
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
popSize = 32
foodGroup = []
popGroup = []
foodSize = 16
circleSize = 12
global simStep
simStep = 1

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

batch2 = pyglet.graphics.Batch()

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

def reproduce(scoreSorted, popNum, mutationRate):
    for i in range(popNum):
        newCircle = agent.Agent(len(entities), 500, 500, batch=batch)
        entities.append(newCircle)
        popGroup.append(newCircle)
        #population2 = sorted(entities, key=lambda x: x.score, reverse=True)
        # newCircle.nn.weights1 = population2[0].nn.weights1
        # newCircle.nn.weights2 = population2[0].nn.weights2
        #parent1 = random.random
        if type(scoreSorted[0]) is agent.Agent and type(scoreSorted[1]) is agent.Agent:
            newCircle.nn.weights1 = spliceArray(scoreSorted[0].nn.weights1, scoreSorted[1].nn.weights1, mutationRate)
            newCircle.nn.weights2 = spliceArray(scoreSorted[0].nn.weights2, scoreSorted[1].nn.weights2, mutationRate)
        else:
            newCircle.nn.weights1 = spliceArray(scoreSorted[0].nn.weights1, scoreSorted[0].nn.weights1, mutationRate)
            newCircle.nn.weights2 = spliceArray(scoreSorted[0].nn.weights2, scoreSorted[0].nn.weights2, mutationRate)


#Build all circle vertex points and store them as vertex lists in batch
def circleEntities(numPop):
    for i in range(numPop):
        newCircle = agent.Agent(i, 500, 500, batch=batch)
        popGroup.append(newCircle)
        entities.append(newCircle)

def generateFood(numFood):
    for f in range(numFood):
        newFood = food.Food(0, x=random.randint(0, 1000), y=random.randint(0, 1000), batch=batch)
        foodGroup.append(newFood)
        entities.append(newFood)

def removeDead():
    toDelete = []
    for e in entities:
        if not e.isActive:
            toDelete.append(e)
    for e in toDelete:
        if e in foodGroup:
            print("Removing Food", foodGroup.index(e))
            foodGroup.remove(e)
            e.delete()
            entities.remove(e)
        elif e in popGroup:
            popGroup.remove(e)



    # for to_remove in [i for i in entities if not i.isActive]:
    #     to_remove.delete()
    #     if to_remove in foodGroup:
    #         print("Removing Food", foodGroup.index(to_remove))
    #         foodGroup.remove(to_remove)
    #     else:
    #         popGroup.remove(to_remove)
    #     entities.remove(to_remove)

# class SimManager():
#     def __init__(self, populationList, foodList):
#         self.populationList = populationList
#         self.foodList = foodList
generateFood(foodSize)
circleEntities(popSize)
uiElements = []
uiElements.append(simUI.infoBox((1010, 990), batch2, foreground))

def update(dt):
    for i in uiElements:
        i.update(dt)
    if not simPause:
        # if len(popGroup) < popSize:
        #     circleEntities(popSize - len(popGroup))
        # elif len(foodGroup) < foodSize:
        #     generateFood(foodSize - len(foodGroup))
        for i in entities:
            i.update(dt, foodGroup)
        removeDead()

        # if len(popGroup) == 0 or len(foodGroup) == 0:
        #     population2 = sorted(entities, key=lambda x: x.score, reverse=True)
        #     print("Finished with score of: ", population2[0].score)
        #     for to_remove in [i for i in entities]:
        #         if to_remove in foodGroup:
        #             foodGroup.remove(to_remove)
        #         if to_remove in popGroup:
        #             popGroup.remove(to_remove)
        #         to_remove.delete()
        #         entities.remove(to_remove)
        #     reproduce(population2, round(popSize * .75), 0.1)
        #     print("Reproduced ", len(entities))
        #     circleEntities(popSize - len(entities))
        #     print("Total Pop: ", len(entities))
        #     generateFood(foodSize)
        #     print("Food: ", len(foodGroup))

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        global simPause
        simPause = not simPause
        print("Sim state toggled")
    if symbol == pyglet.window.key.NUM_1:
        generateFood(1)
    if symbol == pyglet.window.key.NUM_2:
        # newFood = agent2.Agent2(0, x=random.randint(0, 1000), y=random.randint(0, 1000), batch=batch)
        # popGroup.append(newFood)
        # entities.append(newFood)

        newCircle = agent.Agent(-1, 500, 500, batch=batch)
        popGroup.append(newCircle)
        entities.append(newCircle)

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     for e in entities:
#         if e.distance((e.posX, e.posY), (x,y)) < 25:
#             if button == pyglet.window.mouse.LEFT:
#                 uiElements[0].targetCircle = e
#             elif button == pyglet.window.mouse.RIGHT:
#                 print(foodGroup.index(e))
#                 print(e.isActive)

batch2.add(4, pyglet.gl.GL_QUADS, background,
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
