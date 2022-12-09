import pygame
import os
from pygame import mixer
from dino_runner.utils.message import draw_message
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, RESET, GAME_OVER, PLAY_GAME, CLOUD, SOL,  DEFAULT_TYPE, RUNNING_KILLED, STAR, MUSIC_DIR
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 15
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 1100
        self.y_pos_cloud = 130
        
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
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

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.playing = True
        self.score = 0
        self.game_speed = 15

    def run(self):
        self.reset_game()
        #self.obstacle_manager.reset_obstacles()
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
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0:
            self.game_speed += 3


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.draw_cloud()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)     
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

    def draw_cloud(self):
        self.image = CLOUD
        self.image_2 = SOL 
        self.star = STAR
        self.rect = self.image.get_rect()
        self.could_screen_height = SCREEN_HEIGHT
        self.could_screen_width = SCREEN_WIDTH
        self.screen.blit(self.image,(self.could_screen_width -110, self.could_screen_height -520))
        self.screen.blit(self.image,(self.could_screen_width -310, self.could_screen_height -420))
        self.screen.blit(self.image,(self.could_screen_width -510, self.could_screen_height -390))
        self.screen.blit(self.image,(self.could_screen_width -650, self.could_screen_height -450))
        self.screen.blit(self.star,(self.could_screen_width -960, self.could_screen_height -580))
        self.screen.blit(self.image_2,(self.could_screen_width -490, self.could_screen_height -510))
        self.screen.blit(self.image,(self.could_screen_width -790, self.could_screen_height -380))
        self.screen.blit(self.image,(self.could_screen_width -910, self.could_screen_height -420))
        self.screen.blit(self.image,(self.could_screen_width -1090, self.could_screen_height -520))
        
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/ 1000, 2)
            if time_to_show >= 0:
                draw_message(
                    f'{self.player.type.capitalize()} enable for {time_to_show} seconds',
                    self.screen,
                    font_size=18,
                    pos_x_center=880,
                    pos_y_center=80
                )
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE
                pygame.mixer.stop()
                
    def draw_score(self):
        font_score = pygame.font.Font(FONT_STYLE, 30)
        if self.score > self.high_score:
            self.high_score = self.score
        score_print = font_score.render("SCORE: {} |  HIGH SCORE: {}".format(self.score, self.high_score ), True, (0, 255, 255))
        text_rect = score_print.get_rect()
        text_rect.center = (800, 40)
        self.screen.blit(score_print, text_rect)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'music/music_run.mpeg'))
        pygame.mixer.music.play(4)
        pygame.mixer.music.set_volume(0.7)
        font = pygame.font.Font(FONT_STYLE, 30)
        self.screen.fill((0, 0, 0))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        if self.death_count == 0:
            start_print = font.render('PRESS ENTER TO START, YOU HAVE 10 ATTEMPTS', True, (255, 255, 255))
            start_rect = start_print.get_rect()
            start_rect.center = (half_screen_width -10, half_screen_height -200)
            self.screen.blit(start_print, start_rect)
            self.screen.blit(PLAY_GAME,(half_screen_width -65, half_screen_height +35))
        else:
            pass
        if self.death_count <= 4 and self.death_count >= 1:
            death_count = font.render("DEATHS: {}".format(self.death_count), True, (255, 255, 255))
            death_rect = death_count.get_rect()
            death_rect.center = (half_screen_width - 10, half_screen_height - 150)
            self.screen.blit(death_count, death_rect)

        if self.death_count <= 4 and self.death_count >= 1:
            retry_intent = font.render("PRESS ENTER TO RETRY ", True, (255, 255, 255))
            intent_rect = retry_intent.get_rect()
            intent_rect.center = (half_screen_width + 10, half_screen_height + 130)
            self.screen.blit(retry_intent, intent_rect)
            self.screen.blit(RESET,(half_screen_width -50, half_screen_height +35))

        elif self.death_count == 5:
            finish = font.render("YOU DIED MORE THAN 10 TIMES", True, (255, 255, 255))
            finish_game =  finish.get_rect()
            finish_game.center = (half_screen_width + 10, half_screen_height + 130)
            self.screen.blit(finish, finish_game)
            self.screen.blit(GAME_OVER,(half_screen_width -170, half_screen_height +35))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.playing = False
                    self.running = False
        else:
            pass

        self.screen.blit(RUNNING_KILLED,(half_screen_width -80, half_screen_height -80))
        pygame.display.update()
        self.handle_events_on_menu()