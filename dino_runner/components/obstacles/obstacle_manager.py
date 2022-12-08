import random
import pygame
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        
    def update(self, game):
        turn = random.randint(0, 2)
        if len(self.obstacles) == 0:
            if turn == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif turn ==1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 305))
            else:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False
                break
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)