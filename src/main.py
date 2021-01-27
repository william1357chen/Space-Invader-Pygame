import pygame
from pygame import mixer

# gfxdraw is used to create shapes will different alpha values
from pygame import gfxdraw

import math
import time
import os 

base_path = os.path.dirname(__file__)

"""
Future Updates
1. Add more enemies 

2. Add enemy spaceships who can shoot lasers

3. Add barriers 

4. Use Rect objects to improve collision precision

5. Improve runtime 
"""


# initialize pygame
pygame.init()

# create window
screen = pygame.display.set_mode((800, 600))

# note that 800 is width and 600 is height of window, like (x,y)
# all coordinates starts from the top left of the window
# x value increases from left to right
# y value increases from top to bottom

# Change Title
pygame.display.set_caption("Space Invaders")

# Load icon
icon = pygame.image.load(os.path.join(base_path, "images/ufo.png"))

# Set icon on window
pygame.display.set_icon(icon)

# Load Background Image
# The fastest format for .blit() is the same pixel format as the display Surface
# It is a good idea to convert all Surfaces before .blit() many times (from pygame Docs)
background = pygame.image.load(os.path.join(base_path, "images/background.png")).convert()

# Background Sound
mixer.music.load(os.path.join(base_path, "sounds/background.wav"))
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Load Player, Bullet, and Enemy images
playerImg = pygame.image.load(os.path.join(base_path, "images/spaceship.png")).convert()
bulletImg = pygame.image.load(os.path.join(base_path, "images/bullet.png")).convert()
enemyImg = pygame.image.load(os.path.join(base_path, "images/enemy.png")).convert()


# Players Class
class Player:
    def __init__(self):
        self.X = 370
        self.Y = 480
        # horizontal change of spaceship
        self.X_change = 0
        # spaceship does not move vertical so no vertical change

    def set_x_movement(self, X):
        self.X_change = X

    def move_player(self):
        self.X += self.X_change

    def draw_player(self):
        # .convert() defaults the pixel format which creates a white box around spaceship
        # use .set_colorkey() to the color white transparent
        playerImg.set_colorkey((255,255,255))
        screen.blit(playerImg, (self.X, self.Y))

    def check_boundary(self):
        # prevent the spaceship from going out the screen
        if self.X <= 0:
            self.X = 0
        elif self.X >= 736:
            self.X = 736


# Bullet Class
class Bullet:
    def __init__(self):
        self.X = 0
        self.Y = 480 + 10
        self.Y_change = -0.4
        # False means bullet is not drawn on screen
        # True means bullet is fired and currently moving
        self.state = False

    def fire(self, X):
        if self.state is False:
            bullet_sound = mixer.Sound(os.path.join(base_path, "sounds/laser.wav"))
            bullet_sound.set_volume(0.3)
            bullet_sound.play()
            self.X = X + 16
            self.state = True
            self.draw_bullet()

    def check_boundary(self):
        # check if bullet if out of the screen
        # use -20 instead of 0 to make it visually smoother
        if self.Y <= -20:
            self.reset()

    def move_bullet(self):
        if self.state is True:
            self.Y += self.Y_change

    def reset(self):
        self.Y = 480 + 10
        self.state = False

    def draw_bullet(self):
        bulletImg.set_colorkey((255, 255, 255))
        screen.blit(bulletImg, (self.X, self.Y))


# Enemy Class
class Enemy:
    def __init__(self, X, Y, level):
        self.X = X
        self.Y = Y
        # enemy will move linearly faster as level increases
        self.X_change = 0.05 * level + 0.1
        self.Y_change = 60

    def move_enemy_x(self):
        self.X += self.X_change

    def move_enemy_y(self):
        self.Y += self.Y_change

    def check_boundary(self):
        # if enemy hits left or right screen wall move down and to opposite direction
        if self.X <= 0:
            self.X_change = -self.X_change
            self.move_enemy_y()
        elif self.X >= 736:
            self.X_change = -self.X_change
            self.move_enemy_y()

    def draw_enemy(self):
        enemyImg.set_colorkey((255, 255, 255))
        screen.blit(enemyImg, (self.X, self.Y))


# Start Button Class
class Button:
    def __init__(self):
        # If mouse is over button: True, else: False
        self.status = False

    # static method are methods that do not depend on an class instance
    @staticmethod
    def draw_button():
        pygame.draw.circle(screen, (255,0,0), (400,300), 5)
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50, 5)
        twenty_sqrt_three = 20 * math.sqrt(3)
        # The coordinates of the sideways triangle is carefully calculated with geometry
        # to fix in the center of the circle
        pygame.draw.polygon(screen, (255, 255, 255), ((400 + (2 / 3 * twenty_sqrt_three), 300), (400 - (twenty_sqrt_three / 3), 320),(400 - (twenty_sqrt_three / 3), 280)))

    # if mouse if over button, have the back of the button light up
    def draw_trans_button(self):
        if self.status:
            gfxdraw.filled_circle(screen, 400, 300, 50, (255, 255, 255, 100))

    @staticmethod
    def is_over(mouse_pos):
        # if the distance between center and mouse_pos is less than the radius of the circle
        # this means the mouse cursor is inside the circle
        distance = math.sqrt((400 - mouse_pos[0])**2 + (300 - mouse_pos[1])**2)
        return distance <= 50


# Class Score
class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.X = 10
        self.Y = 10

    def show_score(self):
        # texts need to be rendered first before drawn on the screen
        score = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (self.X, self.Y))

    def reset(self):
        self.score = 0

    def __iadd__(self, other):
        self.score += other
        return self.score


# Class Text
class Text:
    def __init__(self, fontsize, X, Y, text, color):
        self.font = pygame.font.Font("freesansbold.ttf", fontsize)
        self.X = X
        self.Y = Y
        self.text = text
        self.color = color

    def show_text(self, alpha):
        text = self.font.render(self.text, True, (self.color[0], self.color[1], self.color[2]))
        text.set_alpha(alpha)
        screen.blit(text, (self.X, self.Y))


# Functions called my game_loop()

def bullet_collision(enemy, bullet, score):
    # making the hit box of enemies smaller to prevent ghost hits
    if enemy.X + 20 <= bullet.X + 16 <= enemy.X + 44 and enemy.Y + 44 >= bullet.Y:
        collision_sound = mixer.Sound(os.path.join(base_path, "sounds/explosion.wav"))
        collision_sound.set_volume(0.3)
        collision_sound.play()
        score += 1
        bullet.reset()
        return True
    return False


def player_collision(enemy, player):
    if enemy.Y + 64 >= player.Y and abs(enemy.X - player.X) <= 64:
        collision_sound = mixer.Sound(os.path.join(base_path, "sounds/explosion.wav"))
        collision_sound.set_volume(0.3)
        collision_sound.play()
        return True
    return False


# Loops

"""
Start Loop: Loop with the start button 
Start Loop --> Game Loop if status_code == 1
Start Loop --> quit program if status_code == 0
"""


def start_loop():
    start_button = Button()
    run = True
    # status code: 0 means quit, and 1 means game starts
    status_code = 1
    while run:
        screen.blit(background, (0, 0))
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

        start_button.draw_trans_button()
        start_button.draw_button()

        pygame.display.update()
    return status_code

"""
Game Loop: the actual space invader game is played in this loop
Game Loop --> GameOver Loop if an enemy touches player status_code == 2
Game Loop --> LevelUp Loop if player defeats all enemies status_code == 1
Game Loop --> quit program if status_code == 0
"""


def game_loop(level, score):
    # Initialize Game Objects
    player = Player()
    bullet = Bullet()
    enemies = [Enemy(x, 50, level) for x in range(150, 710, 80)]

    # game loop
    run = True
    # status code: 0 means quit game, 1 means level up, and 2 means game over
    status_code = 1
    while run:

        # Draw background image
        # note that when background is added, the while loop iterations gets slower
        # so the spaceship and enemy will seem to move much slower
        # .convert() made .blit() much faster
        screen.blit(background, (0, 0))

        # event is anything happening in the game window
        # go through the list of events happening in the game window
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
            p_collision = player_collision(enemy, player)
            if p_collision:
                # end game_loop() and start gameover_loop()
                run = False
                status_code = 2

            # bullet collision
            bullet_hit = False
            if bullet.state is True:
                b_collision = bullet_collision(enemy, bullet, score)
                if b_collision:
                    bullet_hit = True

            if bullet_hit:
                enemies.remove(enemy)
            else:
                # enemy movement
                enemy.move_enemy_x()
                enemy.check_boundary()
                enemy.draw_enemy()

        # bullet movement
        bullet.move_bullet()
        bullet.check_boundary()

        if bullet.state is True:
            bullet.draw_bullet()

        # player movement
        player.move_player()
        player.check_boundary()
        player.draw_player()

        score.show_score()
        # Need to update window for each iteration for changes to happen
        pygame.display.update()

    return status_code

"""
GameOver Loop: shows game over animation
GameOver Loop --> Start Loop if status_code == 1
GameOver Loop --> quit program if status_code == 0
"""


def gameover_loop(score):
    # status code: 0 means quit game, and 1 means go back to start
    status_code = 1
    text = text = Text(64, 200, 250, "GAME OVER", (255,255,255))
    run = True
    alpha_text = 0
    reverse = False
    while run:
        for event in pygame.event.get():
            # if there is an event on the quit red button, quit program
            if event.type == pygame.QUIT:
                run = False
                status_code = 0

        screen.blit(background, (0, 0))
        text.show_text(alpha_text)
        score.show_score()

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

"""
Level Up Loop: shows level up animation
Level Up --> Game Loop if status_code == 1
Level Up --> quit program if status_code == 0
"""


def levelup_loop(level):
    # status code: 0 means quit game, and 1 means go back to game_loop
    run = True
    reverse = False
    text = Text(64, 250, 250, "LEVEL: " + str(level), (0, 0, 0))
    alpha_background = 0
    alpha_text = 0
    status_code = 1
    while run:
        for event in pygame.event.get():
            # if there is an event on the quit red button, quit program
            if event.type == pygame.QUIT:
                run = False
                status_code = 0

        screen.blit(background, (0, 0))
        gfxdraw.box(screen, (0, 0, 800, 600), (255, 255, 255, alpha_background))
        text.show_text(alpha_text)

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

"""
Main Loop: contains all the other loops and decides which loop should be running
"""
def main():
    run = True
    # Level and Score are used continuously so it exists in main loop
    level = 1
    score = Score()
    status_code = 1
    game = False
    while run:
        if status_code == 1 and not game:
            status_code = start_loop()
            game = True
        elif status_code == 0:
            run = False

        if status_code == 1 and game:
            status_code = levelup_loop(level)

        if status_code == 1:
            status_code = game_loop(level, score)
            if status_code == 1:
                level += 1
        else:
            run = False
        if status_code == 2:
            status_code = gameover_loop(score)
            score.reset()
            level = 1
            game = False
        elif status_code == 0:
            run = False


if __name__ == "__main__":
    main()

pygame.quit()