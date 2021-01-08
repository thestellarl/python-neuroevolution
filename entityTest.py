import pyglet
import agent
import food

config = pyglet.gl.Config(sample_buffer = 1, samples = 8)
window = pyglet.window.Window(1200, 1000, config = config)

platform = pyglet.window.get_platform()
display = platform.get_default_display()
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
pyglet.clock.schedule_interval(update, 1/60) # update at 60Hz

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        global simPause
        simPause = not simPause
        print("Sim state toggled")
        print(len(foodGroup))
    if symbol == pyglet.window.key.NUM_1:
        generateFood(1)
    if symbol == pyglet.window.key.NUM_2:
        # newFood = agent2.Agent2(0, x=random.randint(0, 1000), y=random.randint(0, 1000), batch=batch)
        # popGroup.append(newFood)
        # entities.append(newFood)

        newCircle = agent.Agent(-1, 500, 500, batch=batch)
        popGroup.append(newCircle)
        entities.append(newCircle)

window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    batch.draw()
    batch2.draw()
    fps_display.draw()

pyglet.app.run()