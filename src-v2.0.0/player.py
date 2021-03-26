import pygame
import os 
base_path = os.path.dirname(__file__)
# Players Class
class Player:
    def __init__(self):
        self.X = 370
        self.Y = 480
        # horizontal change of spaceship
        self.X_change = 0
        # spaceship does not move vertical so no vertical change
        self.playerImg = pygame.image.load(os.path.join(base_path, "images/spaceship.png")).convert()
    def set_x_movement(self, X):
        self.X_change = X

    def move_player(self):
        self.X += self.X_change
        self.check_boundary()

    def draw_player(self, screen):
        # .convert() defaults the pixel format which creates a white box around spaceship
        # use .set_colorkey() to the color white transparent
        self.playerImg.set_colorkey((255,255,255))
        screen.blit(self.playerImg, (self.X, self.Y))

    def check_boundary(self):
        # prevent the spaceship from going out the screen
        if self.X <= 0:
            self.X = 0
        elif self.X >= 736:
            self.X = 736
