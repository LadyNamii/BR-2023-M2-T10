import pygame 
import random
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, IMG_DIR, IMAGEM_FUNDO, TELA1 , SOM_DO_CENARIO
from dino_runner.components.dinosaur import Dinosaur 
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager 
from dino_runner.utils.text_utils import draw_text
from dino_runner.components.powerups.power_up_manager import PowerUpManager            
import os

FONT_STYLE = "freesansbold.ttf"
FONT_SIZE = 22

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()


    def execute(self):
        self.running = True 
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((123, 123, 123))
        self.screen.blit(IMAGEM_FUNDO, (0,0)) 
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    
    def draw_background(self):
        image_width = IMAGEM_FUNDO.get_width()
        self.screen.blit(IMAGEM_FUNDO, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(IMAGEM_FUNDO, (image_width + self.x_pos_bg, self.y_pos_bg)) 
        if self.x_pos_bg <= -image_width:
            self.screen.blit(IMAGEM_FUNDO, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def draw_score(self):
        draw_text(
            f"score: {self.score}",
            self.screen, 
            pos_x_center=1000,
            pos_y_center=50
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_text(
                    f"{self.player.type.capitalize()} enable for {time_to_show} seconds",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
     
    def show_menu(self):
            self.screen.blit(TELA1,(0,0)) 
            self.screen.blit(IMAGEM_FUNDO , (0,0))
            half_screen_height = SCREEN_HEIGHT // 2
            half_screen_width = SCREEN_WIDTH // 2
    
            if self.death_count == 0:   
                font = pygame.font.Font(FONT_STYLE, )
                text = font.render("Press any key to start", True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (half_screen_width, half_screen_height)
                self.screen.blit(text, text_rect)
            else:
                    draw_text(" Press ane key to restar", self.screen, pos_y_center=half_screen_height+ 140)
                    draw_text(f"Sua pontuação: {self.score}", self.screen, pos_y_center=half_screen_height - 400)
                        
                        
            draw_text(f"Contagem de mortes: {self.death_count}", self.screen, pos_y_center=half_screen_height + 100)
                    
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))

            self.handle_events_on_menu() 
                    
            pygame.display.flip()

   



        
