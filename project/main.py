import random
import pygame
import sys
import pygame.draw
import os
import math
from variables import *
from classes import *
from functions import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
menu_button_sound = pygame.mixer.Sound(os.path.join("sounds", "button_1.wav"))
students_count = 0



class all_map():
    def __init__(self, objects):
        """ Конструктор класса all_map
        придает всем объектам нна карте класс all_map, чтобы их можно
        было все одновременно двигать, не двигая персоннажа
        Args:
        objects - объект класса all_map
        """
        self.objects = objects
        self.color = black

    def render(self):
        screen.fill((92, 193, 81))
        for object in self.objects:
            object.draw()

    def forward(self, axis_x, axis_y):
        # функция движения всей карты вперед
        t = True
        for object in self.objects:
            t = t and not (
                    object.x + object.width >= hero.x and object.x <= hero.x and object.y + object.height * 0.4 >= hero.y and object.y <= hero.y + 35)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y -= hero_velocity / FPS / (2 ** 0.5)
                else:
                    object.y -= hero_velocity / FPS
            else:
                pass

    def backward(self, axis_x, axis_y):
        # функция движения всей карты вниз
        t = True
        for object in self.objects:
            t = t and not (
                    object.x + object.width >= hero.x and object.x <= hero.x and object.y + object.height >= hero.y - 15 and object.y + object.height * 0.6 <= hero.y)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y += hero_velocity / FPS / (2 ** 0.5)
                else:
                    object.y += hero_velocity / FPS
            else:
                pass

    def left(self, axis_x, axis_y):
        # функция движения всей карты влево
        t = True
        for object in self.objects:
            t = t and not (
                    object.x <= hero.x + 35 and object.x + object.width * 0.4 >= hero.x and object.y <= hero.y and object.y + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x -= hero_velocity / FPS / (2 ** 0.5)
                else:
                    object.x -= hero_velocity / FPS
            else:
                pass

    def right(self, axis_x, axis_y):
        # функция движения всей карты вправо
        t = True
        for object in self.objects:
            t = t and not (
                    object.x + object.width * 0.6 <= hero.x and object.x + object.width >= hero.x - 15 and object.y <= hero.y and object.y + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x += hero_velocity / FPS / (2 ** 0.5)
                else:
                    object.x += hero_velocity / FPS
            else:
                pass

class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = mouse_size
        self.img = MOUSE
        
    def draw(self):
        if hero.damage_time > 0:
            self.img = EYE
            screen.blit(self.img, (self.x - eye_width / 2, self.y - eye_height / 5))
        else:
            self.img = MOUSE
            screen.blit(self.img, (self.x - self.size / 2, self.y - self.size / 2))

class Trace():
    def __init__(self, x, y, angle):
        self.angle = angle
        self.width = 0
        self.height = 0
        self.bx = x
        self.by = y
        self.x = x
        self.y = y
        self.vx = 40 * math.sin(angle / 180 * math.pi) / FPS * 60
        self.vy = 40 * math.cos(angle / 180 * math.pi) / FPS * 60
        self.time = 0
        self.killed = 0
        self.radius = 60

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def check(self, index, a, enemy):
        if self.killed:
            enemies[level][enemy].trace = 0
            self.delete(index)
        for wall in entities[level]:
            if self.x > wall.x and self.x < wall.x + wall.width and self.y > wall.y and self.y < wall.y + wall.height:
                self.killed = 1
        if (hero.x - self.x) ** 2 + (hero.y - self.y) **2 < self.radius ** 2:
            hero.damage()

    def delete(self, index):
        entities[level].pop(index)
        for enemy in enemies[level]:
            if index < enemy.index:
                enemy.index -= 1

    def draw(self):
        pygame.draw.rect(screen, black,
                         (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, 50, 50))
        return

class Wall():
    def __init__(self, x, y, width, height, number):
        """ Конструктор класса wall
        Args:
        x - положение стены по горизонтали
        y - положение стены по вертикали
        width - длина
        height - высота
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = WALL[number]

    def draw(self):
        # функция рисования стены на карте
        for i in range(self.width // wall_sprite_size):
            for a in range(self.height // wall_sprite_size):
                screen.blit(self.img, (self.x + i * wall_sprite_size - mouse_pos['x'] 
                                   * mouse_impact, self.y + a * wall_sprite_size - mouse_pos['y'] * mouse_impact))

class Enemy():
    def __init__(self, x, y, angle, number, rotation):
        self.angle = angle
        self.width = 0
        self.height = 0
        self.x = x
        self.y = y
        self.x_from = self.x
        self.y_from = self.y
        self.velocity = 50 / FPS
        self.img = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        self.trace = 0
        self.number = number
        self.stan_time = 0
        self.img_0 = pygame.transform.rotate(self.img, self.angle)
        self.moving = 0
        self.rotation = rotation
        self.rotate_time = 7 * FPS + random.randint(-FPS, FPS)
        self.rotate_len = len(self.rotation)
        self.rotate_index = 0
        self.stars = [Star(self.x, self.y, 0), Star(self.x, self.y, 0.4 * math.pi),
        Star(self.x, self.y, 0.8 * math.pi), Star(self.x, self.y, 1.2 * math.pi), 
        Star(self.x, self.y, 1.6 * math.pi),]

    def draw(self):
        screen.blit(self.img, (self.x - hero.length / 2 - mouse_pos['x'] * mouse_impact, self.y - hero.height / 2 - mouse_pos['y'] * mouse_impact))
        if self.stan_time > 0:
            for i in range(len(self.stars)):
                self.stars[i].update()
                screen.blit(STAR, (self.x + self.stars[i].x - mouse_pos['x'] * mouse_impact, self.y + self.stars[i].y - mouse_pos['y'] * mouse_impact))

    def vision(self, a):
        if not self.trace and self.stan_time == 0:
            self.trace = Trace(self.x, self.y, self.angle)
            a.append(self.trace)
            self.index = len(a) - 1
        elif self.stan_time == 0:
            self.trace.move()
            self.trace.check(self.index, a, self.number)

    def stan(self, stan_time):
        self.stan_time = stan_time * FPS
        if self.trace != 0:
            self.trace.delete(self.index)
        if self.stan_time >= 0:
            self.trace = 0
            
    def rotate(self):
        if self.rotate_time <= 0 and self.rotate_len >= 2:
            if self.angle // 1 != self.rotation[self.rotate_index] :
                self.angle += (self.rotation[self.rotate_index] - self.rotation[self.rotate_index - 1]) / FPS
                self.img = pygame.transform.rotate(self.img_0, self.angle)
            else:
                self.rotate_index += 1
                self.rotate_time = 7 * FPS
            if self.rotate_index == self.rotate_len:
                self.rotate_index = 0
                self.rotate_time = 7 * FPS

class Student():
    def __init__(self, x, y, angle):
        self.width = 0
        self.height = 0
        self.x = x
        self.y = y
        self.angle = angle
        self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", "student.png"))
        self.img = pygame.transform.rotate(self.img_0, self.angle)
        self.killed = False
        self.count = 0
        
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

class Tree():
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.img = FLOOR[index]
        
    def draw(self):
        screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact ,self.y - mouse_pos['y'] * mouse_impact))
    
class Floor():
    def __init__(self, x, y, size, number):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.size = size
        self.img = FLOOR[number]
        
    def draw(self):
        for i in range(self.size[1] // floor_sprite_size):
            for a in range(self.size[0] // floor_sprite_size):
                screen.blit(self.img, (self.x + a * floor_sprite_size - mouse_pos['x'] 
                                   * mouse_impact,self.y + i * floor_sprite_size - mouse_pos['y'] * mouse_impact))

def stan(stan_time):
    global stan_cooldown
    for enemy in enemies[level]:
        if hero.x < enemy.x + stan_range and hero.x > enemy.x - stan_range and hero.y < enemy.y + stan_range and hero.y > enemy.y - stan_range:
            enemy.stan(stan_time)
            stan_cooldown = ability_cooldown * FPS
            
def eat():
    for student in students[level]:
        if hero.x < student.x + eat_range and hero.x > student.x - eat_range and hero.y < student.y + eat_range and hero.y > student.y - eat_range:
            student.eat()

def level_1_win():
    global level
    level = 1
    students_count = 0
    level_2()
    
def level_2_win():
    global level
    level = 0
    students_count = 0
    win()

def win():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(outro_img, (0, 0))

        str1 = 'Останусь я бодрым или сон сразит меня - надеюсь, что первокуры'
        str2 = 'посетят пару и доделают все свои проекты.'
        str3 = 'Я прожил этот день свободным от компромиссов и принимаю зас-'
        str4 = 'луженный отдых без жалоб и сожалений.'
        str5 = 'Вы помогли Ивану найти путь к выходу, спасибо.'
        str6 = 'Нажмите ENTER, чтобы продолжить'

        output(str1, 10, 10, (29, 124, 219))
        output(str2, 10, 50, (29, 124, 219))
        output(str3, 10, 90, (29, 124, 219))
        output(str4, 10, 130, (29, 124, 219))
        output(str5, 200, 600, (0, 255, 0))
        output(str6, 350, 700, (0, 0, 0))


        pause_keys = pygame.key.get_pressed()
        if pause_keys[pygame.K_RETURN]:
            show_menu()

        pygame.display.update()
        
def pause():
    pygame.mouse.set_visible(1)
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
            pygame.mouse.set_visible(0)
        pygame.display.update()
        
def show_menu():
    pygame.mouse.set_visible(1)
    menu_background = BG

    level_1_button = Button(100, 50, 300, 75, menu_button_2, menu_button_1, menu_button_sound)
    level_2_button = Button(500, 375, 300, 75, menu_button_5, menu_button_6, menu_button_sound)
    quit_button = Button(900, 700, 210, 67, menu_button_4, menu_button_3, menu_button_sound)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        level_1_button.draw(level_1)
        level_2_button.draw(level_2)
        #quit_button.draw(quit)

        pygame.display.update()

trees = [[Tree(100, 100, 2), Tree(30, 400, 2), Tree(40, 600, 3), Tree(-140, 1000, 3),
          Tree(340, 1200, 3), Tree(170, 880, 2), Tree(90, 1180, 2)], []]
floor = [[Floor(400, 100, [1500, 900], 1), Floor(400, 200, [600, 500], 0)], 
         []]
students = [[Student(450, 250, 30), Student(420, 150, 90)], []]
enemies = [[Enemy(1850, 430, 0, 0, [-90, 0])], []]
walls = [[Wall(400, 200, 600, 40, 0), Wall(360, 60, 40, 980, 0), Wall(400, 660, 200, 40, 0), Wall(960, 200, 40, 480, 0),
                   Wall(700, 660, 1100, 40, 0), Wall(400, 60, 1540, 40, 0),
                    Wall(400, 1000, 1500, 40, 0), Wall(1900, 60, 40, 980, 0),
                    Wall(1000, 500, 800, 200, 0), Wall(1100, 200, 800, 200, 0)], [Wall(1000, 500, 800, 200, 0)]]
mouse = Mouse(hero.x, hero.y)
entities = [trees[0] + floor[0] + students[0] + walls[0] + doors[0] + enemies[0], trees[1] + floor[1] + students[1] + walls[1] + doors[1] + enemies[1]]
clock = pygame.time.Clock()

def intro():
    pygame.mouse.set_visible(1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(intro_img, (0, 0))

        str1 = 'Этот ФОПФ боится меня. Я видел его истинное лицо, коридоры - '
        str2 = 'продолжение сточных канав, а канавы заполнены жареными кры-'
        str3 = 'сами. И когда все дедлайны будут окончательно слиты,'
        str4 = 'то весь этот плебс начнёт тонуть... Когда скопившиеся долги'
        str5 = 'вспенятся им до пояса, все первокуры посмотрят вверх '
        str6 = 'и возопят:'
        str7 = '"СПАСИ НАС, ИВАН!"'
        str8 = 'А я прошепчу:'
        str9 = 'КАК ЖЕ ХОЧЕТСЯ ПОСПАТЬ...'
        str10 = 'Нажмите ENTER, чтобы продолжить'

        output(str1, 10, 10, (0, 175, 0))
        output(str2, 10, 50, (0, 175, 0))
        output(str3, 10, 90, (0, 175, 0))
        output(str4, 10, 130, (0, 175, 0))
        output(str5, 10, 170, (0, 175, 0))
        output(str6, 10, 210, (0, 175, 0))
        output(str7, 10, 250, (0, 175, 0))
        output(str8, 10, 290, (0, 175, 0))
        output(str9, 600, 600, (255, 175, 0))
        output(str10, 350, 700, (0, 0, 0))

        pause_keys = pygame.key.get_pressed()
        if pause_keys[pygame.K_RETURN]:
            show_menu()

        pygame.display.update()

def level_1():
    global sin, cos, angle, stan_cooldown, axis, students_count, level
    pygame.mouse.set_visible(0)
    level = 0
    mymap = all_map(entities[level])
    scripts = {'forward': mymap.forward, 'backward': mymap.backward, 'left': mymap.left, 'right': mymap.right}
    while level == 0:
        clock.tick(FPS)
        hero.time += 1
        if mouse_pos['x'] != 0:
            if sin > 0:
                angle = math.pi - math.asin((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
                sin = (mouse_pos['x']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
                cos = (mouse_pos['y']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
            else:
                angle = math.asin((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
                sin = (mouse_pos['x']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
                cos = (mouse_pos['y']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
        elif cos // 1 == -1:
            angle = -math.pi / 2
            sin = 0
            cos = -1
        else:
            angle = math.pi / 2
            sin = 0
            cos = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                for key in buttons:
                    if event.key == buttons[key]:
                        flag[key] = 1
                        if (flag['left'] == 1 or flag['right'] == 1) and flag['left'] != flag['right']:
                            axis['Oy'] = 1
                        if (flag['forward'] == 1 or flag['backward'] == 1) and flag['forward'] != flag['backward']:
                            axis['Ox'] = 1
                    if event.key == pygame.K_f:
                        if stan_cooldown == 0:
                            stan(5)
                        eat()
                    if event.key == pygame.K_ESCAPE:
                        pause()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos['x'], mouse_pos['y'] = event.pos[0] - screen_width / 2, event.pos[1] - screen_height / 2
                mouse.x = event.pos[0]
                mouse.y = event.pos[1]

            if event.type == pygame.KEYUP:
                for key in buttons:
                    if event.key == buttons[key]:
                        flag[key] = 0
                        if (flag['left'] != 1 and flag['right'] != 1) or flag['left'] == flag['right']:
                            axis['Oy'] = 0
                        if (flag['forward'] != 1 and flag['backward'] != 1) or flag['forward'] == flag['backward']:
                            axis['Ox'] = 0

        for key in flag:
            if flag[key]:
                scripts[key](axis['Ox'], axis['Oy'])
                hero.sprite_update()

        mymap.render()
        hero.rotate(sin, cos, angle)
        hero.draw(sin, cos, angle)
        if stan_cooldown > 0:
            stan_cooldown -= 1
        for enemy in enemies[level]:
            enemy.vision(entities[level])
            enemy.rotate()
            if enemy.stan_time == 0:
                enemy.rotate_time -= 1
            if enemy.stan_time > 0:
                enemy.stan_time -= 1
            if stan_cooldown == 0 and hero.x < enemy.x + stan_range and hero.x > enemy.x - stan_range and hero.y < enemy.y + stan_range and hero.y > enemy.y - stan_range:
                screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
                font = pygame.font.Font(None, 30)
                name_text = font.render('ОГЛУШИТЬ F', 1, (0, 0, 0))
                screen.blit(name_text, (hero.x - 70, hero.y * 2 - 69))
                
        for student in students[level]:
            if not student.killed and hero.x < student.x + eat_range and hero.x > student.x - eat_range and hero.y < student.y + eat_range and hero.y > student.y - eat_range:
                screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
                font = pygame.font.Font(None, 30)
                name_text = font.render('СЪЕСТЬ F', 1, (0, 0, 0))
                screen.blit(name_text, (hero.x - 55, hero.y * 2 - 69))
        
        for door in doors[level]:
            if hero.x < door.x - 5 + door.width_0 and hero.x > door.x + 5 and hero.y < door.y - 5 + door.height_0 and hero.y > door.y + 5:
                level_1_win()
        
        screen.blit(STUDENTS_BUTTON, (10, 10))
        font = pygame.font.Font('game_font.ttf', 25)
        name_text = font.render('СТУДЕНТОВ СЪЕДЕНО: ' + str(students_count) + " ИЗ " + str(len(students)), 1, (0, 0, 0))
        screen.blit(name_text, (35, 35))
        mouse.draw()
        pygame.display.update()
        hero.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        if hero.damage_time >= 0:
            hero.damage_time -= 1


def level_2():
    global sin, cos, angle, stan_cooldown, axis, students_count, level
    pygame.mouse.set_visible(0)
    level = 1
    mymap = all_map(entities[level])
    scripts = {'forward': mymap.forward, 'backward': mymap.backward, 'left': mymap.left, 'right': mymap.right}
    while level == 1:
        clock.tick(FPS)
        hero.time += 1
        if mouse_pos['x'] != 0:
            if sin > 0:
                angle = math.pi - math.asin((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
                sin = (mouse_pos['x']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
                cos = (mouse_pos['y']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
            else:
                angle = math.asin((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
                sin = (mouse_pos['x']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
                cos = (mouse_pos['y']) / math.sqrt((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2)
        elif cos // 1 == -1:
            angle = -math.pi / 2
            sin = 0
            cos = -1
        else:
            angle = math.pi / 2
            sin = 0
            cos = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                for key in buttons:
                    if event.key == buttons[key]:
                        flag[key] = 1
                        if (flag['left'] == 1 or flag['right'] == 1) and flag['left'] != flag['right']:
                            axis['Oy'] = 1
                        if (flag['forward'] == 1 or flag['backward'] == 1) and flag['forward'] != flag['backward']:
                            axis['Ox'] = 1
                    if event.key == pygame.K_f:
                        if stan_cooldown == 0:
                            stan(5)
                        eat()
                    if event.key == pygame.K_ESCAPE:
                        pause()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos['x'], mouse_pos['y'] = event.pos[0] - screen_width / 2, event.pos[1] - screen_height / 2
                mouse.x = event.pos[0]
                mouse.y = event.pos[1]

            if event.type == pygame.KEYUP:
                for key in buttons:
                    if event.key == buttons[key]:
                        flag[key] = 0
                        if (flag['left'] != 1 and flag['right'] != 1) or flag['left'] == flag['right']:
                            axis['Oy'] = 0
                        if (flag['forward'] != 1 and flag['backward'] != 1) or flag['forward'] == flag['backward']:
                            axis['Ox'] = 0

        for key in flag:
            if flag[key]:
                scripts[key](axis['Ox'], axis['Oy'])
                hero.sprite_update()

        mymap.render()
        hero.rotate(sin, cos, angle)
        hero.draw(sin, cos, angle)
        if stan_cooldown > 0:
            stan_cooldown -= 1
        for enemy in enemies[level]:
            enemy.vision(entities[level])
            enemy.rotate()
            if enemy.stan_time == 0:
                enemy.rotate_time -= 1
            if enemy.stan_time > 0:
                enemy.stan_time -= 1
            if stan_cooldown == 0 and hero.x < enemy.x + stan_range and hero.x > enemy.x - stan_range and hero.y < enemy.y + stan_range and hero.y > enemy.y - stan_range:
                screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
                font = pygame.font.Font(None, 30)
                name_text = font.render('ОГЛУШИТЬ F', 1, (0, 0, 0))
                screen.blit(name_text, (hero.x - 70, hero.y * 2 - 69))
                
        for student in students[level]:
            if not student.killed and hero.x < student.x + eat_range and hero.x > student.x - eat_range and hero.y < student.y + eat_range and hero.y > student.y - eat_range:
                screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
                font = pygame.font.Font(None, 30)
                name_text = font.render('СЪЕСТЬ F', 1, (0, 0, 0))
                screen.blit(name_text, (hero.x - 55, hero.y * 2 - 69))
        
        for door in doors[level]:
            if hero.x < door.x - 5 + door.width_0 and hero.x > door.x + 5 and hero.y < door.y - 5 + door.height_0 and hero.y > door.y + 5:
                level_1_win()
        
        screen.blit(STUDENTS_BUTTON, (10, 10))
        font = pygame.font.Font('game_font.ttf', 25)
        name_text = font.render('СТУДЕНТОВ СЪЕДЕНО: ' + str(students_count) + " ИЗ " + str(len(students)), 1, (0, 0, 0))
        screen.blit(name_text, (35, 35))
        mouse.draw()
        pygame.display.update()
        hero.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        if hero.damage_time >= 0:
            hero.damage_time -= 1
        




flag = {'forward': 0, 'backward': 0, 'left': 0, 'right': 0}
buttons = {'forward': pygame.K_s, 'backward': pygame.K_w, 'left': pygame.K_d, 'right': pygame.K_a}
axis = {'Ox': 0, 'Oy': 0}

intro()

pygame.display.update()
