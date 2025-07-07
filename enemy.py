import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/img/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT:
            self.kill()