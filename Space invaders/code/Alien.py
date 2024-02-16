import pygame

class Alien(pygame.sprite.Sprite):

    def __init__(self, color, x, y):
        super().__init__()
        file_path = '../graphics/' + color + '.png'
        self.image = pygame.image.load(f"{file_path}")
        self.rect = self.image.get_rect(topleft = (x, y))

        if color == 'green': self.value = 100
        elif color == 'yellow': self.value = 200
        else: self.value = 300

    def update(self, alien_speed):
        self.rect.x -= alien_speed



class ExtraAlien(pygame.sprite.Sprite):

    def __init__(self, side):
        super().__init__()
        self.image = pygame.image.load('../graphics/extra.png').convert_alpha()

        if side == 'right':
            x = 650
            self.speed = -2
        elif side == 'left':
            x = -50
            self.speed = 2
        self.rect = self.image.get_rect(topleft = (x, 80))


    def update(self):
        self.rect.x += self.speed