import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed

        # initialize the laser sprite
        self.lasers = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_cooldown = 600
        self.laser_time = 0

        # laser sound
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.1)

    # controls movement of the player
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.shoot_laser()
            self.laser_sound.play(1)
            self.laser_ready = False
            self.laser_time = pygame.time.get_ticks()


    # player shoots laser beams
    def shoot_laser(self):
        self.lasers.add(Laser(laser_width = 3, laser_height = 18, pos = self.rect.midtop, color= 'red', move_speed= -6, height_y_constraint= self.rect.bottom))

    # check if laser in ready again
    def check_laser(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.laser_time >= self.laser_cooldown:
            self.laser_ready = True

    # keeps the player within screen boundaries
    def player_boundary(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= 600:
            self.rect.right = 600

    # updates all the player methods
    def update(self):
        self.get_input()
        self.player_boundary()
        self.check_laser()
        self.lasers.update()






