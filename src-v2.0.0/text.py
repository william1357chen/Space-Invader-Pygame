import pygame 

# Class Text
class Text:
    def __init__(self, font = "", fontsize = 0, X = 0, Y = 0, text = "", color = (0,0,0)):
        self.font = pygame.font.Font(font, fontsize)
        self.X = X
        self.Y = Y
        self.text = text
        self.color = color

    def show_text(self, screen, alpha):
        text = self.font.render(self.text, True, (self.color[0], self.color[1], self.color[2]))
        text.set_alpha(alpha)
        screen.blit(text, (self.X, self.Y))
