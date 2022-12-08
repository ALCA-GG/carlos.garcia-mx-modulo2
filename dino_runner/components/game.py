import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.running =  False
        self.score = 0
        self.high_score = 0
        self.death_count = 0
        game_over = False

    def execute(self):
        self.running =  True

        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()


    def run(self):
        self.obstacle_manager.reset_obstacles()
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input= pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0:
            self.game_speed += 5


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0,0,0))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)    
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        
    def draw_score(self):
        font_score = pygame.font.Font(FONT_STYLE, 30)
        if self.score > self.high_score:
            self.high_score = self.score
        score_print = font_score.render("SCORE: {} |  HIGH SCORE: {}".format(self.score, self.high_score ), True, (0, 255, 255))
        text_rect = score_print.get_rect()
        text_rect.center = (800, 60)
        self.screen.blit(score_print, text_rect)
        
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()
    def show_menu(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            start_print = font.render('PRESS A KEY TO START', True, (0, 0, 0))
            start_rect = start_print.get_rect()
            start_rect.center = (half_screen_width -10, half_screen_height -200)
            self.screen.blit(start_print, start_rect)
        else:
            pass
        if self.death_count >= 0:
            death_count = font.render("DEATHS: {}".format(self.death_count), True, (0, 0, 0))
            death_rect = death_count.get_rect()
            death_rect.center = (half_screen_width - 10, half_screen_height + 150)
            self.screen.blit(death_count, death_rect)
        if self.death_count >= 1:
            retry_intent = font.render("PRESS A KEY TO RETRY ", True, (0, 0, 0))
            intent_rect = retry_intent.get_rect()
            intent_rect.center = (half_screen_width + 10, half_screen_height + 200)
            self.screen.blit(retry_intent, intent_rect)
        else:
            pass

        self.screen.blit(ICON,(half_screen_width -50, half_screen_height -80))
        pygame.display.update()
        self.handle_events_on_menu()