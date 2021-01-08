import random
import math
import pyglet
import entity
from pyglet.gl import *
import numpy
import simUI

config = pyglet.gl.Config(sample_buffer = 1, samples = 8)
window = pyglet.window.Window(1200, 1000, config = config)

platform = pyglet.window.get_platform()
display = platform.get_default_display()
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
fps_display = pyglet.clock.ClockDisplay()

simPause = False
entities = []

batch = pyglet.graphics.Batch()
