from pygame import mixer 
import os 
base_path = os.path.dirname(__file__)
class Music:
    def __init__(self):

        mixer.music.load(os.path.join(base_path, "sounds/background.wav"))
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)

        self.bullet_sound = mixer.Sound(os.path.join(base_path, "sounds/laser.wav"))
        self.collision_sound = mixer.Sound(os.path.join(base_path, "sounds/explosion.wav"))

    def play_bullet_sound(self):
        self.bullet_sound.set_volume(0.3)
        self.bullet_sound.play()

    def play_collision_sound(self):
        self.collision_sound.set_volume(0.3)
        self.collision_sound.play()
    