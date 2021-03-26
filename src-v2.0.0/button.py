import pygame 
from pygame import gfxdraw
import math 
# Start Button Class
class Button:
    def __init__(self):
        # If mouse is over button: True, else: False
        self.status = False

    # static method are methods that do not depend on an class instance
    @staticmethod
    def draw_button(screen):
        pygame.draw.circle(screen, (255,0,0), (400,300), 5)
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50, 5)
        twenty_sqrt_three = 20 * math.sqrt(3)
        # The coordinates of the sideways triangle is carefully calculated with geometry
        # to fix in the center of the circle
        pygame.draw.polygon(screen, (255, 255, 255), ((400 + (2 / 3 * twenty_sqrt_three), 300), (400 - (twenty_sqrt_three / 3), 320),(400 - (twenty_sqrt_three / 3), 280)))

    # if mouse if over button, have the back of the button light up
    def draw_trans_button(self, screen):
        gfxdraw.filled_circle(screen, 400, 300, 50, (255, 255, 255, 100))

    @staticmethod
    def is_over(mouse_pos):
        # if the distance between center and mouse_pos is less than the radius of the circle
        # this means the mouse cursor is inside the circle
        distance = math.sqrt((400 - mouse_pos[0])**2 + (300 - mouse_pos[1])**2)
        return distance <= 50
