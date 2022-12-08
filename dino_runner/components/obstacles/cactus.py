import random
from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, image, rect_y = 325):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = rect_y
