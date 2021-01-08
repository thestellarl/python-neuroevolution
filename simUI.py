import pyglet

class ui:

    def __init__(self, pos, batch, group):
        self.pos = pos
        self.width = 180
        self.height = 980
        self.textScale = 1
        self.batch = batch
        self.targetCircle = None
        self.vertexList = batch.add(4, pyglet.gl.GL_QUADS, group,
                  ('v2f', self.calcVerts(pos))
                  )


    def calcVerts(self, pos):
        # return (self.pos[0] - self.width / 2, self.pos[1] - self.height / 2,
        #         self.pos[0] + self.width / 2, self.pos[1] - self.height / 2,
        #         self.pos[0] + self.width / 2, self.pos[1] + self.height / 2,
        #         self.pos[0] - self.width / 2, self.pos[1] + self.height / 2)
        return (self.pos[0], self.pos[1],
                self.pos[0] + self.width, self.pos[1],
                self.pos[0] + self.width, self.pos[1] - self.height,
                self.pos[0], self.pos[1] - self.height)

    def delete(self):
        self.vertexList.delete()


class infoBox(ui):
    def __init__(self, pos, batch, group):
        super().__init__(pos, batch, group)
        self.label = pyglet.text.Label(str(),
                                  font_name='Arial',
                                  font_size=12,
                                  x= self.pos[0] + self.width/2, y= self.pos[1]-200,
                                  anchor_x='center', anchor_y='center',
                                  color= (0, 0, 0, 255),
                                  batch = batch, group = group)

        self.w1 = batch.add_indexed(7, pyglet.gl.GL_LINES, group, [0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 1, 4, 1, 5, 1, 6, 2, 3, 2, 4, 2, 5, 2, 6], 'v2f/static', 'c4B/static')

        self.w1.vertices = (self.pos[0] + self.width / 2, self.pos[1] - 225,
                            self.pos[0] + 50 + self.width / 2, self.pos[1] - 225,
                            self.pos[0] - 50 + self.width / 2, self.pos[1] - 225,
                            self.pos[0] - 75 + self.width / 2, self.pos[1] - 375,
                            self.pos[0] - 25 + self.width / 2, self.pos[1] - 375,
                            self.pos[0] + 25 + self.width / 2, self.pos[1] - 375,
                            self.pos[0] + 75 + self.width / 2, self.pos[1] - 375)

        self.w1ColorVerts = [0, 0, 0, 255]
        self.w1.colors = self.buildColorVertex(self.w1, self.w1ColorVerts)

        self.w2 = batch.add_indexed(6, pyglet.gl.GL_LINES, group, [0, 2, 0, 3, 0, 4, 0, 5, 1, 2, 1, 3, 1, 4, 1, 5],
                                    'v2f/static', 'c4B/static')
        self.w2.vertices = (self.pos[0] + 50 + self.width / 2, self.pos[1] - 575,
                            self.pos[0] - 50 + self.width / 2, self.pos[1] - 575,
                            self.pos[0] - 75 + self.width / 2, self.pos[1] - 425,
                            self.pos[0] - 25 + self.width / 2, self.pos[1] - 425,
                            self.pos[0] + 25 + self.width / 2, self.pos[1] - 425,
                            self.pos[0] + 75 + self.width / 2, self.pos[1] - 425)
        self.w2ColorVerts = [0, 0, 0, 255]
        self.w2.colors = self.buildColorVertex(self.w2, self.w2ColorVerts)

        self.label2 = pyglet.text.Label(str(),
                                       font_name='Arial',
                                       font_size=12,
                                       x=self.pos[0] + self.width / 2, y=self.pos[1] - 400,
                                       anchor_x='center', anchor_y='center',
                                       color=(0, 0, 0, 255),
                                       batch=batch, group=group)
        self.label3 = pyglet.text.Label(str(),
                                        font_name='Arial',
                                        font_size=12,
                                        x=self.pos[0] + self.width / 2, y=self.pos[1] - 600,
                                        anchor_x='center', anchor_y='center',
                                        color=(0, 0, 0, 255),
                                        batch=batch, group=group)
    def buildColorVertex(self, vertexList, colorVerts):
        while vertexList.get_size() * 4 > len(colorVerts):
            colorVerts += colorVerts[0:4]
        return colorVerts

    def update(self, dt):
        if self.targetCircle is not None:
            l1 = tuple(map(lambda x: round(x, 2), self.targetCircle.nn.input))
            self.label.text = str(l1)
            l2 = tuple(map(lambda x: round(x, 2), self.targetCircle.nn.layer1))
            self.label2.text = str(l2)
            l3 = tuple(map(lambda x: round(x, 2), self.targetCircle.nn.output))
            self.label3.text = str(l3)
            self.targetCircle.nn.weights1
        #self.label.x = self.parent.posX
        #self.label.y = self.parent.posY
        #self.vertexList.vertices = self.calcVerts([self.parent.posX, self.parent.posY])
