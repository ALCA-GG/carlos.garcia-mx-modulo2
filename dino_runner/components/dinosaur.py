import pygame
from dino_runner.utils.constants import RUNNING, JUMPING

class Dinosaur:
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = 310
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = 8.5
    
    def update(self, user_input):
        
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
            
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

        if self.step_index >=10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        
        if self.jump_vel < -8.5:
            self.dino_rect.y = 310
            self.dino_jump = False
            self.jump_vel = 8.5
        
    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect.x = 80
        self.dino_rect.y = 310
        self.step_index += 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))