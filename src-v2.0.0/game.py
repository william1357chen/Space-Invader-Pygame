import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet
from button import Button
from score import Score
from text import Text
from screen import Screen
from music import Music
import time

class Game:
    font = "freesansbold.ttf"
    def __init__(self):
        self.score = Score()
        self.level = 1
        self.screen = Screen()
        self.music = Music()

    def bullet_collision(self, enemy, bullet):
        # making the hit box of enemies smaller to prevent ghost hits
        if enemy.X + 20 <= bullet.X + 16 <= enemy.X + 44 and enemy.Y + 44 >= bullet.Y:
            self.music.play_collision_sound()
            self.score += 1
            bullet.reset()
            return True
        return False

    def player_collision(self, enemy, player):
        if enemy.Y + 64 >= player.Y and abs(enemy.X - player.X) <= 64:
            self.music.play_collision_sound()
            return True
        return False

    def start_loop(self):
        start_button = Button()
        run = True
        # status code: 0 means quit, and 1 means game starts
        status_code = 1
        while run:
            for event in pygame.event.get():
                # if there is an event on the quit red button, quit program
                if event.type == pygame.QUIT:
                    run = False
                    status_code = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hit = pygame.mouse.get_pressed(3)
                    mouse_position = pygame.mouse.get_pos()
                    if hit[0] and start_button.is_over(mouse_position):
                        run = False
                        status_code = 1
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    start_button.status = start_button.is_over(mouse_position)

            self.screen.screen_update_start(start_button)
            pygame.display.update()
        return status_code

    def game_loop(self):
        # Initialize Game Objects
        player = Player()
        bullet = Bullet()
        enemies = [Enemy(x, 50, self.level) for x in range(150, 710, 80)]

        # game loop
        run = True
        # status code: 0 means quit game, 1 means level up, and 2 means game over
        status_code = 1
        while run:
            for event in pygame.event.get():
                # if there is an event on the quit red button, quit program
                if event.type == pygame.QUIT:
                    run = False
                    status_code = 0
                # keystroke events (spaceship movements and bullet fire)
                if event.type == pygame.KEYDOWN:  # if a key is pressed
                    if event.key == pygame.K_LEFT:
                        player.set_x_movement(-0.4)
                    if event.key == pygame.K_RIGHT:
                        player.set_x_movement(0.4)
                    if event.key == pygame.K_SPACE:
                        self.music.play_bullet_sound()
                        bullet.fire(player.X)
                if event.type == pygame.KEYUP:  # if the key is released
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.set_x_movement(0)

            # check if there are any enemies left. If not, game_loop() end and levelup_loop() starts
            if len(enemies) == 0:
                run = False
                status_code = 1
                time.sleep(2)

            # check two types of collisions, bullet or player
            for enemy in enemies:
                # player collision
                p_collision = self.player_collision(enemy, player)
                if p_collision:
                    # end game_loop() and start gameover_loop()
                    run = False
                    status_code = 2

                # bullet collision
                bullet_hit = False
                if bullet.state is True:
                    b_collision = self.bullet_collision(enemy, bullet)
                    if b_collision:
                        bullet_hit = True

                if bullet_hit:
                    enemies.remove(enemy)
                else:
                    # enemy movement
                    enemy.move_enemy_x()
            # bullet movement
            bullet.move_bullet()
            # player movement
            player.move_player()

            self.screen.screen_update_game(player, enemies, bullet, self.score)
            pygame.display.update()
        return status_code

    def gameover_loop(self):
        # status code: 0 means quit game, and 1 means go back to start
        status_code = 1
        text = Text(font = self.font, fontsize = 64, X = 200, Y = 250, text = "GAME OVER", color = (255,255,255))
        run = True
        alpha_text = 0
        reverse = False
        while run:
            for event in pygame.event.get():
                # if there is an event on the quit red button, quit program
                if event.type == pygame.QUIT:
                    run = False
                    status_code = 0
            self.screen.screen_update_gameover(text, alpha_text, self.score)
            # Creates Fade-In and Fade-Out animation
            if not reverse:
                alpha_text += 1
            else:
                alpha_text -= 1
                if alpha_text == 0:
                    run = False
                    time.sleep(2)
            if alpha_text == 255:
                reverse = True
            pygame.display.update()
            time.sleep(0.01)
        return status_code

    def levelup_loop(self):
        # status code: 0 means quit game, and 1 means go back to game_loop
        run = True
        reverse = False
        text = Text(font = self.font, fontsize = 64, X = 250, Y = 250, text = "LEVEL: " + str(self.level), color = (0,0,0))
        alpha_background = 0
        alpha_text = 0
        status_code = 1
        while run:
            for event in pygame.event.get():
                # if there is an event on the quit red button, quit program
                if event.type == pygame.QUIT:
                    run = False
                    status_code = 0
            self.screen.screen_update_levelup(text, alpha_text, alpha_background)
            # Creates Fade-In and Fade-Out animation
            if not reverse:
                if alpha_background < 127:
                    alpha_background += 1
                alpha_text += 1
            else:
                if alpha_background > 0 and alpha_text <= 127:
                    alpha_background -= 1
                alpha_text -= 1
                if alpha_text == 0:
                    run = False
            if alpha_text == 255:
                reverse = True
            pygame.display.update()
            time.sleep(0.01)
        return status_code

    def main(self):
        self.screen.screen_setup()

        run = True
        status_code = 1
        game = False
        while run:
            if status_code == 1 and not game:
                status_code = self.start_loop()
                game = True
            elif status_code == 0:
                run = False

            if status_code == 1 and game:
                status_code = self.levelup_loop()

            if status_code == 1:
                status_code = self.game_loop()
                if status_code == 1:
                    self.level += 1
            else:
                run = False
            if status_code == 2:
                status_code = self.gameover_loop()
                self.score.reset()
                self.level = 1
                game = False
            elif status_code == 0:
                run = False
