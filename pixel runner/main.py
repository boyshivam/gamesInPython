import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("UltimatePygameIntro/graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("UltimatePygameIntro/graphics/Player/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("UltimatePygameIntro/graphics/Player/jump.png").convert_alpha()
        self.player_walks = [player_walk1, player_walk2]
        self.player_index = 0
        self.image = self.player_walks[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("UltimatePygameIntro/audio/jump.mp3")
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walks): self.player_index = 0
            self.image = self.player_walks[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load("UltimatePygameIntro/graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("UltimatePygameIntro/graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos = 120

        else:
            snail_1 = pygame.image.load("UltimatePygameIntro/graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("UltimatePygameIntro/graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom  = (random.randint(900, 1100), self.y_pos))

    def obstacle_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.obstacle_animation()
        self.rect.x -= 6
        self.destroy()

# function to keep track of the score
def get_score():
    current_score = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = text_font.render(f"SCORE: {current_score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_score

# function for movement of the obstacles
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list

    else:
        return []

# function for the collision logic between player and obstacle
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()

pygame.display.set_caption("pixel runner")
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# background music
bg_music = pygame.mixer.Sound("UltimatePygameIntro/audio/music.wav")
bg_music.play(loops=-1)
bg_music.set_volume(0.3)
# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# create sky and ground
sky_surf = pygame.image.load('UltimatePygameIntro/graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('UltimatePygameIntro/graphics/ground.png').convert_alpha()

# text font
text_font = pygame.font.Font("UltimatePygameIntro/font/Pixeltype.ttf", 50)
text_surface = text_font.render(f"Score:", False, (64, 64, 64))
text_rect = text_surface.get_rect(center=(400, 50))


start_time = 0
score = 0

# create obstacles list
obstacles_list = []

# create snail
snail_x = 700
snail_1 = pygame.image.load("UltimatePygameIntro/graphics/snail/snail1.png").convert_alpha()
snail_2 = pygame.image.load("UltimatePygameIntro/graphics/snail/snail2.png").convert_alpha()
snail_movement = [snail_1, snail_2]
snail_index = 0
snail_surf = snail_movement[snail_index]
snail_rect = snail_surf.get_rect(midbottom = (snail_x, 300))

# create flies
fly_x = 700
fly_1 = pygame.image.load("UltimatePygameIntro/graphics/Fly/Fly1.png").convert_alpha()
fly_2 = pygame.image.load("UltimatePygameIntro/graphics/Fly/Fly2.png").convert_alpha()
fly_movement = [fly_1, fly_2]
fly_index = 0
fly_surf = fly_movement[fly_index]
fly_rect = fly_surf.get_rect(midtop = (fly_x, 120))

# timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

game_active = False
#game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail', 'snail'])))

                
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: game_active = True
                snail_rect.left = 800
                fly_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        ## showing items on screen
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # continuously update the score
        score = get_score()

        # obstacle movement
        obstacles_rect_list = obstacle_movement(obstacles_list)

        # check for collisions
        game_active = collision_sprite()


        # draw player class
        player.draw(screen)
        player.update()

        # draw obstacle class
        obstacle_group.draw(screen)
        obstacle_group.update()

    else:
        # game over screen background color
        screen.fill((0, 0, 0))
        obstacles_list.clear()

        # game title
        game_title_surf = text_font.render("The pixel runner", False, (59, 126, 226))
        game_title_rect = game_title_surf.get_rect(center = (400, 40))
        screen.blit(game_title_surf, game_title_rect)

        # pixel runner standing position
        player_stand = pygame.image.load("UltimatePygameIntro/graphics/Player/player_stand.png")
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center = (400, 200))
        screen.blit(player_stand, player_stand_rect)


        # display the score of last game session
        last_score_surf = text_font.render(f"Score: {score}", False, (59, 126, 226))
        last_score_rect = last_score_surf.get_rect(center = (400, 350))
        screen.blit(last_score_surf, last_score_rect)

    pygame.display.update()
    clock.tick(60)
