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

def output(text, x, y, font_color, font_type='game_font.ttf', font_size=27):
    font_type = pygame.font.Font(font_type, font_size)
    message1 = font_type.render(text, True, font_color)
    message2 = font_type.render(text, True, (0,0,0))
    screen.blit(message2, (x+1, y+1))
    screen.blit(message1, (x, y))
        

