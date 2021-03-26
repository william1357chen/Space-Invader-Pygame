import pygame 
from pygame import gfxdraw
import os 

base_path = os.path.dirname(__file__)

class Screen:
    def __init__(self, width = 800, height = 600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load(os.path.join(base_path, "images/background.png")).convert()
        self.title = "Space Invaders v1.0.0"
    def screen_setup(self):
        self.load_icon()
        self.set_window_caption()
    
    def set_window_caption(self):
        pygame.display.set_caption(self.title)
    
    @staticmethod
    def load_icon():
        icon = pygame.image.load(os.path.join(base_path, "images/ufo.png"))
        pygame.display.set_icon(icon)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_player(self, player):
        player.draw_player(self.screen)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            enemy.draw_enemy(self.screen)
    def draw_bullet(self, bullet):
        bullet.draw_bullet(self.screen)

    def draw_button(self, button):
        if button.status is True:
            button.draw_trans_button(self.screen)
        button.draw_button(self.screen)

    def draw_score(self, score):
        score.show_score(self.screen)

    def draw_text(self, text, alpha_text):
        text.show_text(self.screen, alpha_text)

    def draw_white_background(self, alpha_background):
        gfxdraw.box(self.screen, (0, 0, 800, 600), (255, 255, 255, alpha_background))

    def screen_update_start(self, button):
        self.draw_background()
        self.draw_button(button)
        

    def screen_update_game(self, player, enemies, bullet, score):
        self.draw_background()
        self.draw_player(player)
        self.draw_enemies(enemies)
        self.draw_bullet(bullet)
        self.draw_score(score)
        

    def screen_update_gameover(self, text, alpha_text, score):
        self.draw_background()
        self.draw_text(text, alpha_text)
        self.draw_score(score)

    def screen_update_levelup(self, text, alpha_text, alpha_background):
        self.draw_background()
        self.draw_white_background(alpha_background)
        self.draw_text(text, alpha_text)

