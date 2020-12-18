import random
import pygame
import sys
import pygame.draw
import os
import math
from variables import *
from functions import *

screen = pygame.display.set_mode((screen_width, screen_height))


class Door():
    def __init__(self, x, y, width, height, angle):
        self.angle = angle
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width_0 = 100
        self.height_0 = 100
        self.opened = False
        self.img = pygame.transform.rotate(STAIRS, self.angle)
        
    def draw(self):
        screen.blit(self.img, (self.x - mouse_pos['x'] 
                                   * mouse_impact, self.y - mouse_pos['y'] * mouse_impact))
        if self.opened:
            return
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, self.width, self.height))

    def door_open(self):
        self.opened = True
        self.width = 0
        self.height = 0
        
class Hero():
    def __init__(self, cos, sin, angle):
        """ Конструктор класса hero
        """
        self.hp = 3
        self.length = 56
        self.height = 56
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.color = black
        self.cos = cos
        self.sin = sin
        self.angle = (angle / math.pi) * 180 - 90
        self.time = 0
        self.damage_time = 0
        self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        self.eye = EYE
        self.health_bar = HEALTH_BAR

    def rotate(self, cos, sin, angle):
        self.cos = cos
        self.sin = sin
        self.angle = (angle / math.pi) * 180 - 90
        self.img = pygame.transform.rotate(self.img_0, self.angle)

    def draw(self, cos, sin, angle):
        if self.hp > 0:
            screen.blit(self.health_bar[self.hp - 1], (20, hero.y * 2 - health_sprite_height - 20))
        screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact - self.length / 2,
                               self.y - mouse_pos['y'] * mouse_impact - self.height / 2))
        self.mask = pygame.mask.from_surface(self.img)
        

    def hero_update(self, x, y):
        self.x += mouse_pos['x'] * mouse_impact
        self.y += mouse_pos['y'] * mouse_impact

    def sprite_update(self):
        if (self.time // 8) % 5 == 1:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[1]))
        elif (self.time // 8) % 5 == 2:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[2]))
        elif (self.time // 8) % 5 == 3:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[3]))
        elif (self.time // 8) % 5 == 4:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[4]))
        else:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
            
    def damage(self):
        if self.damage_time <= 0:
            self.hp -= 1
            self.damage_time = 2 * FPS

class Star():
    def __init__(self, x, y, angle):
        self.radius = 23
        self.angle = angle
        self.x = self.radius * math.sin(self.angle) - 5
        self.y = self.radius * math.cos(self.angle)
        self.img = STAR
        
    def update(self):
        self.x = self.radius * math.sin(self.angle) - 5
        self.y = self.radius * math.cos(self.angle)
        self.angle += math.pi / FPS * 3

        

doors = [[Door(1800, 100, 10, 100, -90)], [Door(2000, 1200, 100, 10, 180)]]




hero = Hero(sin, cos, angle)
