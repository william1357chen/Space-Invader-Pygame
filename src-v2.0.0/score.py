import pygame 
# Class Score
class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.X = 10
        self.Y = 10

    def show_score(self, screen):
        # texts need to be rendered first before drawn on the screen
        score = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (self.X, self.Y))

    def reset(self):
        self.score = 0

    def __iadd__(self, other):
        self.score += other
        return self

