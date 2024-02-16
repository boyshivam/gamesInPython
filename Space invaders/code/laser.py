import pygame


class Laser(pygame.sprite.Sprite):

    def __init__(self, laser_width, laser_height,  pos, color, move_speed, height_y_constraint):
        super().__init__()
        self.image = pygame.Surface((laser_width, laser_height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.move_speed = move_speed
        self.height_y_constraint = height_y_constraint


    # configures the direction of the laser movement
    def laser_movement(self):
        self.rect.y += self.move_speed

    # destroy laser beams
    def destroy_laser(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.laser_movement()
        self.destroy_laser()
