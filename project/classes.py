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

    def rotate(self, cos, sin, angle):
        self.cos = cos
        self.sin = sin
        self.angle = (angle / math.pi) * 180 - 90
        self.img = pygame.transform.rotate(self.img_0, self.angle)

    def draw(self, cos, sin, angle):
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
            if self.hp <= 0:
                lose()

class Student():
    def __init__(self, x, y, angle):
        self.width = 0
        self.height = 0
        self.x = x
        self.y = y
        self.angle = angle
        self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        self.img = pygame.transform.rotate(self.img_0, self.angle)
        self.killed = False
        
    def draw(self):
        if not self.killed:
            screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact - hero.length / 2,
                               self.y - mouse_pos['y'] * mouse_impact - hero.height / 2))
        
    def eat(self):
        global students_count
        if not self.killed:
            self.killed = True
            students_count += 1
            if students_count == len(students[level]):
                for door in doors[level]:
                    door.door_open()

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

class Button:
    def __init__(self, x, y, width, height, active_img, inactive_img, sound):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_img = inactive_img
        self.active_img = active_img
        self.sound = sound

    def draw(self, func=None) -> object:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            screen.blit(self.active_img, (self.x, self.y))

            if click[0] == 1:
                pygame.mixer.Sound.play(self.sound)
                pygame.time.delay(400)
                if func is not None:
                    func()

        else:
            screen.blit(self.inactive_img, (self.x, self.y))

        

doors = [[Door(1800, 100, 10, 100, -90)], []]
students = [[Student(450, 250, 30), Student(420, 150, 90)], []]



hero = Hero(sin, cos, angle)
