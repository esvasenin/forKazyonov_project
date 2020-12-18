import random
import pygame
import sys
import pygame.draw
import os
import math
from classes import *
from variables import *

pygame.mixer.init()
menu_button_sound = pygame.mixer.Sound(os.path.join("sounds", "button_1.wav"))
screen = pygame.display.set_mode((screen_width, screen_height))


def output(text, x, y, font_color, font_type='game_font.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    message = font_type.render(text, True, font_color)
    screen.blit(message, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(p_menu, (0, 0))

        output('ВЫ ПРИОСТАНОВИЛИ ИГРУ', 130, 30, (0, 209, 224))
        output('Чтобы продолжить жмякните ENTER', 400, 425, (255, 0, 0))

        menu_butt = Button(1100, 850, 190, 35, esc_menu_button_1, esc_menu_button_2, menu_button_sound)

        menu_butt.draw(show_menu)

        pause_keys = pygame.key.get_pressed()
        if pause_keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        
def lose():
    return
