import pygame, sys
from me import Me
from enemy import Enemy, Enemy1
from random import choice, randint
from shooting import Shot

class Game:
    def __init__(self):
        # Игрок
        my_sprite = Me((screen_width / 2, screen_height), screen_width, 6)
        self.me = pygame.sprite.GroupSingle(my_sprite)
        # Жизни
        self.hps = 3
        self.hp_dsp = pygame.image.load('../space_invaders-main/pics/heart.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.hp_dsp.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('../space_invaders-main/shrift/dot.ttf', 30)
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        # Противники
        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()
        self.enemy_setting(rows=4, cols=6)
        self.enemy_direct = 1
        # Корабль
        self.enemy1 = pygame.sprite.GroupSingle()
        self.enemy1_spwn_tm = randint(40, 80)
        # Звук
        sound = pygame.mixer.Sound('../space_invaders-main/sound/background.wav')
        sound.play(loops=-1)
        self.shot_sound = pygame.mixer.Sound('../space_invaders-main/sound/shoot.wav')
        self.hit_sound = pygame.mixer.Sound('../space_invaders-main/sound/hit.wav')

    def enemy_setting(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    enemy_sprite = Enemy('enemy1', x, y)
                elif 1 <= row_index <= 2:
                    enemy_sprite = Enemy('enemy2', x, y)
                else:
                    enemy_sprite = Enemy('enemy3', x, y)
                self.enemies.add(enemy_sprite)

    def enemy_pos(self):
        all_enemies = self.enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= screen_width:
                self.enemy_direct = -1
                self.enemy_go_down(3)
            elif enemy.rect.left <= 0:
                self.enemy_direct = 1
                self.enemy_go_down(3)

    def enemy_go_down(self, row_d):
        if self.enemies:
            for enemy in self.enemies.sprites():
                enemy.rect.y += row_d



    def enemy_shooting(self):
        if self.enemies.sprites():
            rand_enemy = choice(self.enemies.sprites())
            shot_sprite = Shot(rand_enemy.rect.center, 6, screen_height)
            self.enemy_shots.add(shot_sprite)
            self.shot_sound.play()

    def enemy1_time(self):
        self.enemy1_spwn_tm -= 1
        if self.enemy1_spwn_tm <= 0:
            self.enemy1.add(Enemy1(choice(['right', 'left']), screen_width))
            self.enemy1_spwn_tm = randint(550, 950)

    def hits(self):
        # Лазер игрока
        if self.me.sprite.shots:
            for shot in self.me.sprite.shots:
                if pygame.sprite.spritecollide(shot, self.blocks, True):
                    shot.kill()
                # Попадания противник
                enemy_hit = pygame.sprite.spritecollide(shot, self.enemies, True)
                if enemy_hit:
                    for enemy in enemy_hit:
                        self.score += enemy.exp
                    shot.kill()
                    self.hit_sound.play()
                # Попадания корабль
                if pygame.sprite.spritecollide(shot, self.enemy1, True):
                    self.score += 500
                    shot.kill()
        # Лазер противника
        if self.enemy_shots:
            for shot in self.enemy_shots:
                #
                if pygame.sprite.spritecollide(shot, self.blocks, True):
                    shot.kill()

                if pygame.sprite.spritecollide(shot, self.me, False):
                    shot.kill()
                    self.hps -= 1
                    if self.hps <= 0:
                        pygame.quit()
                        sys.exit()
        # Противники
        if self.enemies:
            for enemy in self.enemies:
                pygame.sprite.spritecollide(enemy, self.blocks, True)

                if pygame.sprite.spritecollide(enemy, self.me, False):
                    pygame.quit()
                    sys.exit()

    def show_hp(self):
        for live in range(self.hps - 1):
            x = self.live_x_start_pos + (live * (self.hp_dsp.get_size()[0] + 10))
            screen.blit(self.hp_dsp, (x, 8))

    def show_highscore(self):
        highscore_dsp = self.font.render(f'highscore: {self.score}', False, 'green')
        score_rect = highscore_dsp.get_rect(topleft=(250, -1))
        screen.blit(highscore_dsp, score_rect)

    def again(self):
        if not self.enemies.sprites():
            self.enemies = pygame.sprite.Group()
            self.enemy_shots = pygame.sprite.Group()
            self.enemy_setting(rows=4, cols=6)
            self.enemy_direct = 1

    def start(self):
        self.me.update()
        self.enemy_shots.update()
        self.enemy1.update()

        self.enemies.update(self.enemy_direct)
        self.enemy_pos()
        self.enemy1_time()
        self.hits()

        self.me.sprite.shots  .draw(screen)
        self.me.draw(screen)
        self.blocks.draw(screen)
        self.enemies.draw(screen)
        self.enemy_shots.draw(screen)
        self.enemy1.draw(screen)
        self.show_hp()
        self.show_highscore()
        self.again()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    enemy_shoot = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_shoot, 800)#

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == enemy_shoot:
                game.enemy_shooting()
        screen.fill((0, 40, 0))
        game.start()
        pygame.display.flip()
        clock.tick(60)