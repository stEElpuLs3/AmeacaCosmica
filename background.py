# background.py

import pygame
from settings import *

class Background:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        # Para um efeito de parallax vertical, a imagem deve ter a mesma largura da tela
        # e, idealmente, pelo menos a mesma altura.
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        
        self.speed = speed
        
        # O truque para a rolagem infinita é usar duas cópias da imagem.
        # Uma começa na tela e a outra logo acima.
        self.rect1 = self.image.get_rect()
        self.rect1.topleft = (0, 0)
        
        self.rect2 = self.image.get_rect()
        self.rect2.topleft = (0, -HEIGHT) # Posiciona a segunda imagem acima da primeira

    def update(self):
        # Move ambas as imagens para baixo
        self.rect1.y += self.speed
        self.rect2.y += self.speed
        
        # Se uma imagem saiu completamente da tela por baixo,
        # ela é reposicionada para cima da outra.
        if self.rect1.top >= HEIGHT:
            self.rect1.y = self.rect2.y - HEIGHT
            
        if self.rect2.top >= HEIGHT:
            self.rect2.y = self.rect1.y - HEIGHT

    def draw(self, surface):
        # Desenha as duas imagens na tela
        surface.blit(self.image, self.rect1)
        surface.blit(self.image, self.rect2)