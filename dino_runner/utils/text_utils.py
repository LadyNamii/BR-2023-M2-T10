import pygame

from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH

FONT_COLOR = (0,0,0)
FONT_SIZE = 22
FONT_STYLE = "freesansbold.ttf"


def draw_text( message, screen, size= FONT_SIZE , pos_x_center=SCREEN_WIDTH // 2, pos_y_center=SCREEN_HEIGHT // 2, color=FONT_COLOR  ):

        font = pygame.font.Font(FONT_STYLE, size)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos_x_center, pos_y_center)
        screen.blit(text_surface, text_rect)
                

        