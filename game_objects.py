# Scripts
from constants import *
from background import *

# Modules
import pygame
from pygame import mixer
import random

# Initialize Pygame
pygame.init()


class Player:
    hp = 3  # Player HP
    y_enter = 19/18 * HEIGHT
    Δd = 0

    def __init__(self, image, pos, Δpos):
        self.image = pygame.image.load(image)
        self.l_image = self.image.get_rect().width
        self.pos = pos
        self.Δpos = Δpos
        self.init_d = 0.3 * dt

        # HP Bar
        self.hp_bar_pos = (1/43 * WIDTH, 16/17 * HEIGHT)
        self.hp_bar_size = (108, 30)
        self.hp_bar_border_color = (255, 255, 255)    # White
        self.hp_bar_low_color = (255, 49, 49)  # Neon Red
        self.hp_bar_med_color = (255, 165, 0)  # Orange
        self.hp_bar_full_color = (15, 255, 80)     # Neon Green
        self.line_width = 2
        self.border_radius = 4

    def show_image(self, x, y):
        SCREEN.blit(self.image, (x, y))

    def draw_hp_bar(self, hp):
        x_1, y_1 = (self.hp_bar_pos[0] + 1/3 * self.hp_bar_size[0], self.hp_bar_pos[1])
        x_2, y_2 = (x_1, y_1 + self.hp_bar_size[1] - 1)

        x_3, y_3 = (self.hp_bar_pos[0] + 2/3 * self.hp_bar_size[0], y_1)
        x_4, y_4 = (x_3, y_2)

        Δinner_pos = 4
        Δinner_size = 8.5
        inner_pos_1 = (self.hp_bar_pos[0] + 5, self.hp_bar_pos[1] + Δinner_pos)
        inner_pos_2 = (self.hp_bar_pos[0] + self.hp_bar_pos[0] + 1/6 * self.hp_bar_size[0], self.hp_bar_pos[1] + Δinner_pos)
        inner_pos_3 = (self.hp_bar_pos[0] + self.hp_bar_pos[0] + 1/2 * self.hp_bar_size[0], self.hp_bar_pos[1] + Δinner_pos)
        inner_size_1 = (1/3 * self.hp_bar_size[0] - Δinner_size + 1, self.hp_bar_size[1] - Δinner_size)
        inner_size_2 = (1/3 * self.hp_bar_size[0] - Δinner_size + 1, self.hp_bar_size[1] - Δinner_size)
        inner_size_3 = (1/3 * self.hp_bar_size[0] - Δinner_size, self.hp_bar_size[1] - Δinner_size)

        pygame.draw.line(SCREEN, self.hp_bar_border_color, (x_1, y_1), (x_2, y_2), self.line_width)
        pygame.draw.line(SCREEN, self.hp_bar_border_color, (x_3, y_3), (x_4, y_4), self.line_width)
        pygame.draw.rect(SCREEN, self.hp_bar_border_color, (*self.hp_bar_pos, *self.hp_bar_size), self.line_width, 4)

        if hp == 3:
            pygame.draw.rect(SCREEN, self.hp_bar_full_color, (*inner_pos_1, *inner_size_1))
            pygame.draw.rect(SCREEN, self.hp_bar_full_color, (*inner_pos_2, *inner_size_2))
            pygame.draw.rect(SCREEN, self.hp_bar_full_color, (*inner_pos_3, *inner_size_3))
        elif hp == 2:
            pygame.draw.rect(SCREEN, self.hp_bar_med_color, (*inner_pos_1, *inner_size_1))
            pygame.draw.rect(SCREEN, self.hp_bar_med_color, (*inner_pos_2, *inner_size_2))
        elif hp == 1:
            pygame.draw.rect(SCREEN, self.hp_bar_low_color, (*inner_pos_1, *inner_size_1))


class PlayerBullet:
    image = []
    pos = []
    Δpos = []
    # Time Delay to Shoot Player Bullet
    p_bullet_ref = 30   # Initial Reference

    def __init__(self, image, Δpos, Δt_p_bullet):
        self.image = pygame.image.load(image)
        self.l_image = self.image.get_rect().width
        self.x = 0
        self.y = 480
        self.Δpos = Δpos
        self.Δt_p_bullet = Δt_p_bullet
        self.sound = mixer.Sound('Sounds/laser.wav')
        self.col_sound = mixer.Sound('Sounds/explosion.wav')

    def fire_bullet(self):
        for i in range(len(PlayerBullet.pos[:])):
            SCREEN.blit(PlayerBullet.image[i], (PlayerBullet.pos[i], PlayerBullet.pos[i]))

    def generate_bullet(self):
        PlayerBullet.image.append(self.image)
        PlayerBullet.pos.append([player.pos[0] + 16, player.pos[1] + 10])
        #PlayerBullet.Δpos.append((self.Δpos[0], self.Δpos[1]))


class Enemy:
    enemy_list = []
    image = []
    pos = []
    Δpos = []
    Δt_bullet = []

    # Define time delay between enemies to spawn: 8.0 sec
    time_to_spawn = 4000
    spawn_enemy = pygame.USEREVENT + 0
    pygame.time.set_timer(spawn_enemy, time_to_spawn)

    def __init__(self):
        self.image = pygame.image.load(enemies_img['common'])
        self.l_image = self.image.get_rect().width
        self.Δx = 0.25 * dt
        self.Δy = 30

    def show_image(self, x, y, i):
        SCREEN.blit(Enemy.image[i], (x, y))

    def generate_enemies(self, n):
        for i in range(0, n):
            Enemy.enemy_list.append(i)
            Enemy.image.append(self.image)
            Enemy.pos.append([random.randint(0, WIDTH - self.l_image), random.randint(-100, 0 - self.l_image)])
            Enemy.Δpos.append([self.Δx, self.Δy])
            Enemy.Δt_bullet.append(0)

class EnemyBullet:
    # Define Bullet Variables
    image = []
    pos = []
    Δpos = []

    def __init__(self):
        self.image = pygame.image.load(enemies_bullet_img['common'])
        self.l_image = self.image.get_rect().width
        self.Δx = 0
        self.Δy = 0.2 * dt
        self.sound = mixer.Sound('Sounds/laser.wav')
        self.col_sound = mixer.Sound('Sounds/explosion.wav')

    def fire_bullet(self):
        for i in range(len(EnemyBullet.pos[:])):
            SCREEN.blit(EnemyBullet.image[i], EnemyBullet.pos[i])

    def generate_bullet(self, i):
        EnemyBullet.image.append(self.image)
        EnemyBullet.pos.append([Enemy.pos[i][0], Enemy.pos[i][1]])
        EnemyBullet.Δpos.append((self.Δx, self.Δy))

class Speakers:
    def __init__(self):
        self.on_image = pygame.image.load('Images/Speakers/speakers_on_img.png')
        self.off_image = pygame.image.load('Images/Speakers/speakers_off_img.png')
        self.position = self.x, self.y = (13/14 * WIDTH, 1/75 * HEIGHT)
        self.on_rect = self.on_image.get_rect(x=self.x, y=self.y)
        self.off_rect = self.off_image.get_rect(x=self.x, y=self.y)
        self.state = "off"      # This means game will begin with Speakers-Off as default
        self.initial_sound = 0.0

    def action(self, x, y, state):
        if state == "off":
            SCREEN.blit(self.off_image, (x, y))
            mixer.music.set_volume(0.0)
            p_bullet.sound.set_volume(self.initial_sound)
            p_bullet.col_sound.set_volume(self.initial_sound)
        elif state == "on":
            SCREEN.blit(self.on_image, (x, y))
            mixer.music.set_volume(0.08)
            p_bullet.sound.set_volume(0.08)
            p_bullet.col_sound.set_volume(0.08)


class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.position = self.x, self.y = (10, 10)

    def show(self, x, y):
        score_screen = self.font.render("Score: " + str(self.value), True, (255, 255, 255))
        SCREEN.blit(score_screen, (x, y))


# Initialize Classes:
# Player
player = Player(
    'Images/Player/player_img.png',    # Image Size: 64 x 64
    [WIDTH/2 - C_64/2, 5/6 * HEIGHT],
    [0, 0]
)

p_bullet = PlayerBullet(
    'Images/Player_Bullet/bullets.png',     # ImageSize: 32 x 32
    [0, 1.2 * dt],
    30
)


enemy = Enemy()
e_bullet = EnemyBullet()
speakers = Speakers()
score = Score()
background = Background()


if __name__ == '__main__':
    pass
