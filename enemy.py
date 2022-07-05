import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemytype, x, y):
        super().__init__()
        file_path = '../space_invaders-main/pics/' + enemytype + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        if enemytype == 'enemy1':
            self.exp = 150
        elif enemytype == 'enemy2':
            self.exp = 100
        else:
            self.exp = 50



    def update(self, direction):
        self.rect.x += direction


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('../space_invaders-main/pics/enemy_up.png').convert_alpha()
# Скорость корабля
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed