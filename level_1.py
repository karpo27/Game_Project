# Scripts
from game_objects import *
from enemies import *


# Modules
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()


def run_level_1():
    # Game Loop
    run = True
    while run:
        # Set screen FPS
        clock.tick(FPS)

        # Define Number of Enemies to spawn in Level 1: 10
        enemies_lvl_1 = [enemies['enemy_b'], enemies['enemy_b']]

        # Draw Scrolling Background
        background.show()

        # Go to Game Over / Continue Screen
        if player.lives < 1:
            pass

        # Consume Life to Keep Playing
        if player.hp == 0:
            player.lives -= 1
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Press Mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos = pygame.mouse.get_pos()
                if speakers.off_rect.collidepoint(mouse_pos):
                    if speakers.state == "off":
                        speakers.state = "on"
                    else:
                        speakers.state = "off"

            # Spawn Enemies According to Level
            if len(enemies_group) < len(enemies_lvl_1):
                if event.type == Enemy.spawn_enemy:
                    k = enemies_lvl_1[len(enemies_group)]
                    # Generate Enemies
                    new_enemy = Enemy(*k)
                    enemies_group.add(new_enemy)

        # Update Sprites
        player.update()

        # Update Sprites Group
        player_bullet_group.update()
        enemies_group.update()
        enemies_bullet_group.update()

        explosion_group.update()

        # Draw Sprite Groups
        enemies_bullet_group.draw(SCREEN)
        enemies_group.draw(SCREEN)

        player_bullet_group.draw(SCREEN)
        player_group.draw(SCREEN)

        explosion_group.draw(SCREEN)

        player.draw_hp_bar(player.hp, player.hp_animation)
        score.show(score.x, score.y)
        speakers.action(speakers.x, speakers.y, speakers.state)

        # Apply changes
        pygame.display.update()


run_level_1()
