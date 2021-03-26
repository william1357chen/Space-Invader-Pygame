import pygame
import os 
base_path = os.path.dirname(__file__)
# Enemy Class
class Enemy:
    def __init__(self, X, Y, level):
        self.X = X
        self.Y = Y
        # enemy will move linearly faster as level increases
        self.X_change = 0.05 * level + 0.1
        self.Y_change = 60
        self.enemyImg = pygame.image.load(os.path.join(base_path, "images/enemy.png")).convert()
    def move_enemy_x(self):
        self.X += self.X_change
        self.check_boundary()

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

    def draw_enemy(self, screen):
        self.enemyImg.set_colorkey((255, 255, 255))
        screen.blit(self.enemyImg, (self.X, self.Y))
