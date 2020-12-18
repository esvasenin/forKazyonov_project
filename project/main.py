import random
import pygame
import sys
import pygame.draw
import os
import math

FPS = 60

screen_width = 1400
screen_height = 900
level_size = [1500, 1500]
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
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
students_count = 0
FLOOR = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor_1.png")), (floor_sprite_size,floor_sprite_size)),
         pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor_2.png")), (floor_sprite_size,floor_sprite_size))]
WALL = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "wall_1.png")), (wall_sprite_size,wall_sprite_size))]
STAIRS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "stairs.jpg")), (100, 100))
menu_button_1 = pygame.image.load(os.path.join("assets", "1lvl.png"))
menu_button_2 = pygame.image.load(os.path.join("assets", "1lvl_dark.png"))
menu_button_3 = pygame.image.load(os.path.join("assets", "esc.png"))
menu_button_4 = pygame.image.load(os.path.join("assets", "esc_dark.png"))

esc_menu_button_1 = pygame.image.load(os.path.join("assets", "back_to_menu_dark.png"))
esc_menu_button_2 = pygame.image.load(os.path.join("assets", "back_to_menu.png"))

menu_button_sound = pygame.mixer.Sound(os.path.join("sounds", "button_1.wav"))


angle = math.pi
sin = 1
cos = 0
ability_cooldown = 10
stan_cooldown = 0
stan_range = 60
eat_range = 40


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
        screen.fill((255, 255, 255))
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
        
        
class Floor():
    def __init__(self, x, y, size, number):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.size = size
        self.sprite = black
        self.img = FLOOR[number]
        
        
    def draw(self):
        for i in range(self.size[1] // floor_sprite_size):
            for a in range(self.size[0] // floor_sprite_size):
                screen.blit(self.img, (self.x + a * floor_sprite_size - mouse_pos['x'] 
                                   * mouse_impact,self.y + i * floor_sprite_size - mouse_pos['y'] * mouse_impact))


class Hero():
    def __init__(self, cos, sin, angle):
        """ Конструктор класса hero
        """
        self.length = 56
        self.height = 56
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.color = black
        self.cos = cos
        self.sin = sin
        self.angle = (angle / math.pi) * 180 - 90
        self.time = 0
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
            print(students_count)
            if students_count == len(students):
                for door in doors:
                    door.door_open()

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

    def draw(self):
        screen.blit(self.img, (self.x - hero.length / 2 - mouse_pos['x'] * mouse_impact, self.y - hero.height / 2 - mouse_pos['y'] * mouse_impact))

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

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def check(self, index, a, enemy):
        if self.killed:
            enemies[enemy].trace = 0
            self.delete(index)
        for wall in entities:
            if self.x > wall.x and self.x < wall.x + wall.width and self.y > wall.y and self.y < wall.y + wall.height:
                self.killed = 1

    def delete(self, index):
        entities.pop(index)
        for enemy in enemies:
            if index < enemy.index:
                enemy.index -= 1

    def draw(self):
        pygame.draw.rect(screen, black,
                         (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, 50, 50))
        return


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


def output(text, x, y, font_color, font_type='game_font.ttf', font_size=40):
    font_type = pygame.font.Font(font_type, font_size)
    message = font_type.render(text, True, font_color)
    screen.blit(message, (x, y))

def stan(stan_time):
    global stan_cooldown
    for enemy in enemies:
        if hero.x < enemy.x + stan_range and hero.x > enemy.x - stan_range and hero.y < enemy.y + stan_range and hero.y > enemy.y - stan_range:
            enemy.stan(stan_time)
            stan_cooldown = ability_cooldown * FPS
            
def eat():
    for student in students:
        if hero.x < student.x + eat_range and hero.x > student.x - eat_range and hero.y < student.y + eat_range and hero.y > student.y - eat_range:
            student.eat()

def win():
    print("win")


def show_menu():
    menu_background = BG

    level_1_button = Button(100, 50, 300, 75, menu_button_2, menu_button_1, menu_button_sound)
    quit_button = Button(900, 700, 210, 67, menu_button_4, menu_button_3, menu_button_sound)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_background, (0, 0))
        level_1_button.draw(level_1)

        pygame.display.update()


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



def level_1():
    global sin, cos, angle, stan_cooldown, axis, students_count

    clock = pygame.time.Clock()
    while 1:
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
        for enemy in enemies:
            enemy.vision(entities)
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
                
        for student in students:
            if not student.killed and hero.x < student.x + eat_range and hero.x > student.x - eat_range and hero.y < student.y + eat_range and hero.y > student.y - eat_range:
                screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
                font = pygame.font.Font(None, 30)
                name_text = font.render('СЪЕСТЬ F', 1, (0, 0, 0))
                screen.blit(name_text, (hero.x - 55, hero.y * 2 - 69))
        
        for door in doors:
            if hero.x < door.x - 5 + door.width_0 and hero.x > door.x + 5 and hero.y < door.y - 5 + door.height_0 and hero.y > door.y + 5:
                win()
        
        screen.blit(STUDENTS_BUTTON, (10, 10))
        font = pygame.font.Font('game_font.ttf', 25)
        name_text = font.render('СТУДЕНТОВ СЪЕДЕНО: ' + str(students_count) + " ИЗ " + str(len(students)), 1, (0, 0, 0))
        screen.blit(name_text, (35, 35))
        pygame.display.update()
        hero.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))

doors = [Door(1800, 100, 10, 100, -90)]
students = [Student(450, 250, 30), Student(420, 150, 90)]
floor = [Floor(400, 100, [1500, 900], 1), Floor(400, 200, [600, 500], 0)]
enemies = [Enemy(1850, 430, 0, 0, [-90, 0])]  #Enemy(400, 230, 250, 0), Enemy(520, 280, 30, [], 1), Enemy(270, 320, 180, 2)
walls = [Wall(400, 200, 600, 40, 0), Wall(360, 60, 40, 980, 0), Wall(400, 660, 200, 40, 0), Wall(960, 200, 40, 480, 0),
                   Wall(700, 660, 1100, 40, 0), Wall(400, 60, 1540, 40, 0),
                    Wall(400, 1000, 1500, 40, 0), Wall(1900, 60, 40, 980, 0),
                    Wall(1000, 500, 800, 200, 0), Wall(1100, 200, 800, 200, 0)]
hero = Hero(sin, cos, angle)
entities = floor + enemies + students + walls + doors
mymap = all_map(entities)

flag = {'forward': 0, 'backward': 0, 'left': 0, 'right': 0}
scripts = {'forward': mymap.forward, 'backward': mymap.backward, 'left': mymap.left, 'right': mymap.right}
buttons = {'forward': pygame.K_s, 'backward': pygame.K_w, 'left': pygame.K_d, 'right': pygame.K_a}
axis = {'Ox': 0, 'Oy': 0}

show_menu()

pygame.display.update()
