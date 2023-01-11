# Scripts
from game_objects import *

# Modules
import pygame
from pygame import mixer
import random

# Initialize Pygame
pygame.init()


def run_level_1():
    # Game Loop
    run = True
    while run:
        # Set screen FPS
        clock.tick(FPS)

        # Draw Scrolling Background
        background.show()

        # Enter Level Animation
        if player.pos[1] < Player.y_enter - Player.Δd:
            pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP])
            player.show_image(player.pos[0], Player.y_enter - Player.Δd)
            Player.Δd += 1.9
        else:
            Player.y_enter = 0
            Player.Δd = 0
            pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])
            player.show_image(player.pos[0], player.pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Press Keyboard
            if event.type == pygame.KEYDOWN:
                # Player Keyboard Movement
                if event.key == pygame.K_LEFT:
                    player.Δpos[0] = -0.3 * dt
                elif event.key == pygame.K_RIGHT:
                    player.Δpos[0] = 0.3 * dt
                elif event.key == pygame.K_UP:
                    player.Δpos[1] = -0.3 * dt
                elif event.key == pygame.K_DOWN:
                    player.Δpos[1] = 0.3 * dt
                # Player Bullet Keyboard
                elif event.key == pygame.K_SPACE:
                    if PlayerBullet.Δt_p_bullet >= PlayerBullet.p_bullet_ref:
                        PlayerBullet.Δt_p_bullet = 0
                        #p_bullet.sound.play()
                        #p_bullet.sound.set_volume(speakers.initial_sound)
                        p_bullet.generate_bullet()

            # Release Keyboard
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.Δpos[0] = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    player.Δpos[1] = 0

            # Press Mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos = pygame.mouse.get_pos()
                if speakers.off_rect.collidepoint(mouse_pos):
                    if speakers.state == "off":
                        speakers.state = "on"
                    else:
                        speakers.state = "off"

            # Define Number of Enemies to spawn in Level 1: 10
            enemies_lvl_1 = ['common', 'common']
            n_enemies = len(enemies_lvl_1)
            if len(Enemy.enemy_list) < n_enemies:
                if event.type == Enemy.spawn_enemy:
                    enemy.generate_enemies(1)

        # Player Movement Boundaries
        player.pos[0] += player.Δpos[0]
        player.pos[1] += player.Δpos[1]

        if player.pos[0] <= 0:
            player.pos[0] = 0
        if player.pos[1] <= 0:
            player.pos[1] = 0
        if player.pos[0] >= WIDTH - player.l_image:
            player.pos[0] = WIDTH - player.l_image
        if player.pos[1] >= HEIGHT - player.l_image:
            player.pos[1] = HEIGHT - player.l_image

        # Player Bullet Movement
        if PlayerBullet.Δt_p_bullet < PlayerBullet.p_bullet_ref:
            PlayerBullet.Δt_p_bullet += 1

        for bullet_pos in PlayerBullet.pos[:]:
            bullet_pos[1] -= p_bullet.Δy

            if bullet_pos[1] < 0:
                PlayerBullet.image.pop()
                PlayerBullet.pos.remove(bullet_pos)
                PlayerBullet.Δpos.pop()

        p_bullet.fire_bullet()

        # Enemies Movement
        for i in range(len(Enemy.enemy_list)):
            Enemy.pos[i][0] += Enemy.Δpos[i][0]

            if Enemy.pos[i][0] <= 0:
                Enemy.Δpos[i][0] = 0.3 * dt
                Enemy.pos[i][1] += Enemy.Δpos[i][1]
            elif Enemy.pos[i][0] >= WIDTH - enemy.l_image:
                Enemy.Δpos[i][0] = -0.3 * dt
                Enemy.pos[i][1] += Enemy.Δpos[i][1]

            # Collision Detection (fix problem at intersection of objects when pressing "spacebar")
            collision = pygame.Rect.colliderect(
                p_bullet.image.get_rect(x=p_bullet.x, y=p_bullet.y),
                enemy.image.get_rect(x=Enemy.pos[i][0], y=Enemy.pos[i][1])
            )
            if collision:
                # The collision will affect only if this:
                if Enemy.pos[i][1] + enemy.l_image >= 0:
                    p_bullet.y = player.y
                    p_bullet.state = "ready"
                    score.value += 1
                    p_bullet.col_sound.play()

            # After Enemies Appear Generate Enemy Bullet every 80 cycles (fix for every enemy later)
            if len(Enemy.enemy_list) > 0:
                Enemy.Δt_bullet[i] += 1
                if Enemy.pos[i][1] >= 0 and Enemy.Δt_bullet[i] >= 80:
                    Enemy.Δt_bullet[i] = 0
                    e_bullet.generate_bullet(i)

            # Show Enemies Images
            enemy.show_image(Enemy.pos[i][0], Enemy.pos[i][1], i)

        # Enemy Bullet Movement
        for bullet_pos in EnemyBullet.pos[:]:
            bullet_pos[1] += e_bullet.Δy

            if bullet_pos[1] > HEIGHT:
                EnemyBullet.image.pop()
                EnemyBullet.pos.remove(bullet_pos)
                EnemyBullet.Δpos.pop()

        e_bullet.fire_bullet()
        # Call Functions
        player.draw_hp_bar(Player.hp)
        score.show(score.x, score.y)
        speakers.action(speakers.x, speakers.y, speakers.state)

        # Apply changes
        pygame.display.update()


run_level_1()
