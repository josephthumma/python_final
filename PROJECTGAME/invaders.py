import pygame
from pygame import mixer
import os
import time
import random
from entities import SpacePlayer, SpaceEnemy, objectcollide

pygame.font.init()
mixer.init()

COLOR_WHITE = (255,255,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (69, 252, 3)

GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_SPEED = 4
ENEMY_SPEED = 1
BULLET_SPEED = 5

GAMESOLDIER = 'gamesoldier'
GAMECAPTAIN = 'gamecaptain'
GAMEBOSS = 'gameboss'

#WINDOW SETUP
WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

#LOAD IMAGES
BACKGROUNDIMAGE = pygame.image.load(os.path.join("assets", "background.jpg"))
UFO_ENEMY = pygame.image.load(os.path.join("assets", "ufo.png"))
ENEMY_UFO_STRONG = pygame.image.load(os.path.join("assets", "ufo_stronger.png"))
ENEMY_UFO_BOSS = pygame.image.load(os.path.join("assets", "ufo_boss.png"))
SPACESHIP_PLAYER = pygame.image.load(os.path.join("assets", "player.png"))

#LOAD SOUNDS
MUSIC = mixer.music.load(os.path.join("assets", "music.mp3"))
LASER_SOUND = mixer.Sound(os.path.join("assets", "laser.wav"))
LASER_SOUND.set_volume(0.1)
EXPLOSION_SOUND = mixer.Sound(os.path.join("assets", "explosion.wav"))
EXPLOSION_SOUND.set_volume(0.2)
mixer.music.play(-1)

def main():
    run = True
    pause = False
    FPS = 60
    level = 0
    lives = 5
    clock = pygame.time.Clock()

    main_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 20)
    game_over_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 28)
    x_player = int((GAME_WIDTH / 2) - (SPACESHIP_PLAYER.get_width() / 2))   #center player horizontally
    y_player = 480
    player = SpacePlayer(x_player, y_player, SPACESHIP_PLAYER)

    spaceenemies=[]
    length_wave = 5
    lost = False
    count_lost = 0

    def draw_window():
        WINDOW.blit(BACKGROUNDIMAGE, (0,0))
        #text
        
        lives_label = main_font.render(f"Lives: {lives}", True , COLOR_WHITE)
        level_label = main_font.render(f"Level: {level}", True, COLOR_WHITE)
        score_label = main_font.render(f"Score: {player.score}", True, COLOR_WHITE)

        WINDOW.blit(lives_label, (10, 10))
        level_label_x = GAME_WIDTH - level_label.get_width() - 10
        WINDOW.blit(level_label, (level_label_x, 10))
        score_label_x = GAME_WIDTH/2 - score_label.get_width()/2
        WINDOW.blit(score_label, (score_label_x, 10))

        #DRAW ENEMIES
        for enemy in spaceenemies:
            enemy.draw(WINDOW)

        #DRAW PLAYER
        player.draw(WINDOW)

        if lost:
            game_over_label = game_over_font.render(f"GAME OVER", True , COLOR_RED)
            WINDOW.blit(game_over_label, ((GAME_WIDTH/2)-(game_over_label.get_width()/2), 
                                            (GAME_HEIGHT/2) - (game_over_label.get_height()/2)))

        if pause:
            pause_label= main_font.render("Game paused...", True , COLOR_WHITE)
            WINDOW.blit(pause_label, ((GAME_WIDTH/2)-(pause_label.get_width()/2), 
                                            (GAME_HEIGHT/2) - (pause_label.get_height()/2)))
            
        pygame.display.update()


    while run:
        clock.tick(FPS)
        draw_window()

        #CHECK REMAINING LIVES
        if lives == 0:
            lost= True
            count_lost += 1

        #take life if health is depleted
        if player.health <= 0 and lives > 0:
            EXPLOSION_SOUND.play()
            lives -= 1
            player.health = 100

        #SHOW GAME OVER MESSAGE FOR 3 SECS THEN QUIT
        if lost:
            if count_lost > FPS * 3:
                run= False
            else:
                continue
        

        #SEND WAVES OF ENEMIES
        if len(spaceenemies) == 0:
            level += 1
            length_wave += 5
            for i in range(length_wave):
                enemy = SpaceEnemy(
                    random.randrange(50, GAME_WIDTH-64), #enemy sprite is 64x64 px
                    random.randrange(-1500, -100), 
                    random.choice([GAMESOLDIER,GAMECAPTAIN,GAMEBOSS]),
                    EXPLOSION_SOUND)
                spaceenemies.append(enemy)

        #CHECK QUIT        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                quit()

        #CHECK PRESSED KEYS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            #MOVE PLAYER LEFT
            if not player.boundary_left():
                player.move_left(PLAYER_SPEED)
            
        if keys[pygame.K_RIGHT]:
            #MOVE PLAYER RIGHT
            if not player.boundary_right(GAME_WIDTH):
                player.move_right(PLAYER_SPEED)

        if keys[pygame.K_DOWN]:
            #MOVE PLAYER DOWN
            if not player.boundary_down(GAME_HEIGHT):
                player.move_down(PLAYER_SPEED)

        if keys[pygame.K_UP]:
            #MOVE PLAYER UP
            if not player.boundary_up():
                player.move_up(PLAYER_SPEED)        

        if keys[pygame.K_SPACE]:
            LASER_SOUND.play()
            player.shoot()
        
        if keys[pygame.K_ESCAPE]:
            pause = not pause

        #pause menu
        if pause:
            continue
        
        #MOVE ENEMIES
        for enemy in spaceenemies[:]:
            enemy.move_down(ENEMY_SPEED)
            enemy.move_lasers(BULLET_SPEED, GAME_HEIGHT, player)

            #enemy shooting chance
            if random.randrange(0, 2*60) == 1:    #enemy shooting probability
                LASER_SOUND.play() 
                enemy.shoot()

            #check collision between enemy and player
            if objectcollide(enemy, player):
                player.health -= 50
                EXPLOSION_SOUND.play()
                spaceenemies.remove(enemy)
                #when enemy leaves the screen remove and take a life
            elif enemy.check_off_screen(GAME_HEIGHT):
                player.health -= 20
                spaceenemies.remove(enemy)


        player.move_lasers(-BULLET_SPEED, GAME_HEIGHT, spaceenemies)

def menu():
    run = True
    font_title = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 60)
    font_subtitle = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 20)
    while run:

        WINDOW.blit(BACKGROUNDIMAGE, (0,0))
        title_label = font_title.render("SPACE INVADERS", True, COLOR_WHITE)
        subtitle_label = font_subtitle.render("press SPACEBAR to begin...", True, COLOR_WHITE)
        WINDOW.blit(title_label, (GAME_WIDTH/2-title_label.get_width()/2, 100))
        WINDOW.blit(subtitle_label, (GAME_WIDTH/2-subtitle_label.get_width()/2, 480))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                main()

        pygame.display.update()

    pygame.quit()


menu()
