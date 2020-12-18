import pygame
import pygame.draw
import os
import math


FPS = 60

screen_width = 1400
screen_height = 900
level_size = [1500, 1500]
black = (0, 0, 0)
white = (255, 255, 255)
hero_size = {'x': 56, 'y': 56}
hero_velocity = 500
mouse_pos = {'x': screen_width / 2, 'y': screen_height / 2}
mouse_impact = 0.15
hero_sprite = ["player_stand.png", "player_walk1.png", "player_walk2.png", "player_walk3.png", "player_walk4.png"]
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (screen_width, screen_height))
STAN_BUTTON = pygame.image.load(os.path.join("sprites", "stan.png"))
p_menu = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pause_menu.png")), (screen_width, screen_height))
STUDENTS_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "students.png")), (468,69))
floor_sprite_size = 100
wall_sprite_size = 20
health_sprite_width = 150
health_sprite_height = 60
students_count = 0
level = 0
eye_width = 180
eye_height = 100
mouse_size = 95
FLOOR = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor_1.png")), (floor_sprite_size,floor_sprite_size)),
         pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor_2.png")), (floor_sprite_size,floor_sprite_size)),
         pygame.image.load(os.path.join("assets", "tree_1.png")), pygame.image.load(os.path.join("assets", "tree_2.png"))]
HEALTH_BAR = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "health_bar_1.png")), (health_sprite_width,health_sprite_height)),
         pygame.transform.scale(pygame.image.load(os.path.join("assets", "health_bar_2.png")), (health_sprite_width,health_sprite_height)),
         pygame.transform.scale(pygame.image.load(os.path.join("assets", "health_bar_3.png")), (health_sprite_width,health_sprite_height))]
WALL = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "wall_1.png")), (wall_sprite_size,wall_sprite_size))]
STAIRS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "stairs.jpg")), (100, 100))
STAR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "star.png")), (15, 15))
MOUSE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mouse.png")), (mouse_size, mouse_size))
EYE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "see_you.png")), (eye_width, eye_height))
menu_button_1 = pygame.image.load(os.path.join("assets", "1lvl.png"))
menu_button_2 = pygame.image.load(os.path.join("assets", "1lvl_dark.png"))
menu_button_3 = pygame.image.load(os.path.join("assets", "esc.png"))
menu_button_4 = pygame.image.load(os.path.join("assets", "esc_dark.png"))
menu_button_5 = pygame.image.load(os.path.join("assets", "2lvl_dark.png"))
menu_button_6 = pygame.image.load(os.path.join("assets", "2lvl.png"))

esc_menu_button_1 = pygame.image.load(os.path.join("assets", "back_to_menu_dark.png"))
esc_menu_button_2 = pygame.image.load(os.path.join("assets", "back_to_menu.png"))

intro_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Pixel_Ivan.png")), (screen_width, screen_height))
outro_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Pixel_Ivan_win.png")), (screen_width, screen_height))


angle = math.pi
sin = 1
cos = 0
ability_cooldown = 10
stan_cooldown = 0
stan_range = 60
eat_range = 40