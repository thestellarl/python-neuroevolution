import entity

class Food(entity.Circle):
    def __init__(self, id, x, y, batch):
        colorCode = [255, 255, 0, 255]
        super().__init__(id, x, y, colorCode, batch)
        foodVal = 1
        self.radius = 10
        self.score = -1

    def update(self, empty, empty2):
        super().update()