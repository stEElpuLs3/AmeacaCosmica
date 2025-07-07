import pygame
from settings import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets_group):
        super().__init__()
        self.image = pygame.image.load('assets/img/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group
        
        self.shoot_sound = pygame.mixer.Sound('assets/snd/shoot.wav')

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.all_sprites.add(bullet)
        self.bullets_group.add(bullet)
        self.shoot_sound.play()