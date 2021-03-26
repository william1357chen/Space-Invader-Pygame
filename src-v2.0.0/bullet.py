import pygame
import os 
base_path = os.path.dirname(__file__)
# Bullet Class
class Bullet:
    def __init__(self):
        self.X = 0
        self.Y = 480 + 10
        self.Y_change = -0.4
        # False means bullet is not drawn on screen
        # True means bullet is fired and currently moving
        self.state = False
        self.bulletImg = pygame.image.load(os.path.join(base_path, "images/bullet.png")).convert()

    def fire(self, X):
        if self.state is False:
            self.X = X + 16
            self.state = True

    def check_boundary(self):
        # check if bullet if out of the screen
        # use -20 instead of 0 to make it visually smoother
        if self.Y <= -20:
            self.reset()

    def move_bullet(self):
        if self.state is True:
            self.Y += self.Y_change
            self.check_boundary()

    def reset(self):
        self.Y = 480 + 10
        self.state = False

    def draw_bullet(self, screen):
        if self.state is True:
            self.bulletImg.set_colorkey((255, 255, 255))
            screen.blit(self.bulletImg, (self.X, self.Y))

