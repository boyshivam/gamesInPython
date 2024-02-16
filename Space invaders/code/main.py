import pygame, sys
from player import Player
import obstacle
from Alien import Alien, ExtraAlien
import random
from laser import Laser

class Game:

    def __init__(self):
        player_sprite = Player((screen_width/2, screen_height), 4)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # obstacle setup
        self.no_of_obstacles = 4
        self.x_offset_positions = [int(num*(screen_width/self.no_of_obstacles)) for num in range(self.no_of_obstacles)]
        self.blocks = pygame.sprite.Group()
        self.block_size = 6
        self.create_multiple_obstacles()

        # score
        self.score = 0
        self.score_font = pygame.font.Font('../font/Pixeled.ttf', size=20)

        # health of player
        self.lives = 3
        self.live_surf = pygame.image.load('../graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*2 + 20)

        # initialize alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(ROWS = 6, COLS = 8)
        self.alien_direction = 1

        # extra alien setup
        self.extra_alien = pygame.sprite.GroupSingle()
        self.extra_alien_spawn = random.randint(40, 80)

        # background sound of the game
        bg_music = pygame.mixer.Sound('../audio/music.wav')
        bg_music.set_volume(0.2)
        bg_music.play(-1)

        # laser sound
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.1)

        # explosion sound
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.4)

    # checks when the extra alien appears on the screen
    def extra_alien_timer(self):
        self.extra_alien_spawn -= 1
        if self.extra_alien_spawn <= 0:
            self.extra_alien.add(ExtraAlien(random.choice(['left', 'right'])))
            self.extra_alien_spawn = random.randint(400, 800)

    # aliens setup on screen
    def alien_setup(self, ROWS, COLS, x_dist = 60, y_dist = 60, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(ROWS)):
            for col_index, col in enumerate(range(COLS)):
                x = col_index*x_dist + x_offset
                y = row_index*y_dist + y_offset

                if row_index == 0: alien = Alien('red', x, y)
                elif 1<= row_index <=2: alien = Alien('yellow', x, y)
                else: alien = Alien('green', x= x, y=y)
                self.aliens.add(alien)

    # maintains the positions of the aliens within the screen
    def aliens_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= 600:
                self.alien_direction = 1
                self.aliens_move_down()
            elif alien.rect.left <= 0:
                self.alien_direction = -1
                self.aliens_move_down()

    # aliens move towards the player
    def aliens_move_down(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            alien.rect.y += 3

    # aliens shoot at the player
    def aliens_shoot(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(3, 8, random_alien.rect.center, 'white', 5, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play(1)
    def create_obstacle(self ,x_dist  ,y_dist, x_offset):
        for row_index, row in enumerate(obstacle.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = col_index*self.block_size + x_dist + x_offset
                    y = row_index*self.block_size + y_dist
                    block = obstacle.Block(size = self.block_size, color = 'green', x_cor = x, y_cor = y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self):
        for offset in self.x_offset_positions:
            self.create_obstacle(x_dist=40, y_dist=500, x_offset=offset)


    def collision_checks(self):
        # lasers from player
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit =pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    self.explosion_sound.play(1 )
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.extra_alien, True):
                    laser.kill()
                    self.explosion_sound.play(1)
                    self.score += 500

        # lasers from aliens
        global game_active
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        game_active = False

        # alien and player collision
        if self.aliens:
            for alien in self.aliens:
                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()
                    sys.exit()

        # alien crosses player territory
        if self.aliens:
            for alien in self.aliens:
                if alien.rect.y >= screen_height:
                    pygame.quit()
                    sys.exit()

    # displays the remaining lives of the player
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live*(self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x,8))

    # displays the current score
    def display_score(self):
        score_surf = self.score_font.render(f'SCORE: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10, -10))
        screen.blit(score_surf, score_rect)


    def check_win(self):
        if not self.aliens.sprites():
            self.winner_text = self.score_font.render('You won!!!', False, 'white')
            self.winner_rect = self.winner_text.get_rect(topleft = (300, 300))
            screen.blit(self.winner_text, self.winner_rect)



    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.aliens.update(self.alien_direction)
        self.extra_alien.update()

        self.collision_checks()
        self.aliens_position_checker()
        self.display_lives()
        self.display_score()
        self.extra_alien_timer()

        self.blocks.draw(screen)
        self.player.draw(screen)
        self.alien_lasers.draw(screen)
        self.aliens.draw(screen)
        self.extra_alien.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.check_win()

class CRT:

    def __init__(self):
        self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()

    def draw(self):
        self.tv.set_alpha(random.randint(75, 90))
        screen.blit(self.tv, (0,0))

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    game = Game()
    crt = CRT()

    ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER, 800)

    game_active = True
    while True:
            if game_active:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == ALIEN_LASER:
                        game.aliens_shoot()

                    if event.type == game.check_win():
                        game_active = False


                screen.fill((30, 30, 30))

                game.run()
                crt.draw()
                pygame.display.flip()
                clock.tick(60)

            else:
                game_over_surf = pygame.Surface((600, 600))
                game_over_surf.fill((50, 50, 0))
                screen.blit(game_over_surf, (0, 0))








