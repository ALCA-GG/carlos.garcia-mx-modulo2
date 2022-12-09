import random
import pygame
import os
from dino_runner.utils.constants import MUSIC_DIR
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, SHIELD_TYPE, HAMMER_TYPE
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
            elif turn ==2:
                self.obstacles.append(Bird(BIRD))
            else:
                pass
        

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    if game.player.type != HAMMER_TYPE:
                        self.sound_kill = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'music/kull.mp3'))
                        self.sound_kill.play()
                        pygame.time.delay(1000)
                        game.playing = False
                        game.death_count +=1
                        game.score = 0
                        game.game_speed = 15
                        break
                    else:
                        self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []