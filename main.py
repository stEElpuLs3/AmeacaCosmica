import pygame
from settings import *
import random
from player import Player
from enemy import Enemy
from background import Background

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ameaça Cósmica - Demo")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

player = Player(all_sprites, bullets_group)
all_sprites.add(player)

SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)
        
score = 0
font = pygame.font.Font(None, 36)
explosion_sound = pygame.mixer.Sound('assets/snd/explosion.wav')

game_state = 'playing'  # Controla o estado atual do jogo
final_score = 0

bg_distante = Background('assets/img/nebula.png', speed=1)
bg_proximo = Background('assets/img/nebula2.png', speed=2)
bg_estrelas = Background('assets/img/nebul.png', speed=4) 
def get_rank_name(score):
    """Retorna um nome de classificação baseado na pontuação."""
    if score < 50:
        return "Piloto Novato"
    elif score < 150:
        return "Cadete Espacial"
    elif score < 300:
        return "Ás dos Asteroides"
    elif score < 500:
        return "Comandante Estelar"
    else:
        return "Lenda Galáctica"

def draw_game_over_screen(surface, score):
    """Desenha a tela de Game Over."""
    font_large = pygame.font.Font(None, 74)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    rank_name = get_rank_name(score)

    game_over_text = font_large.render("GAME OVER", True, RED)
    score_text = font_medium.render(f"Pontuação Final: {score}", True, WHITE)
    rank_text = font_medium.render(f"Classificação: {rank_name}", True, (255, 255, 0)) # Amarelo
    instruction_text = font_small.render("Pressione qualquer tecla para reiniciar", True, WHITE)

    # Centralizando os textos
    game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
    score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    rank_rect = rank_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
    instruction_rect = instruction_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))

    surface.blit(game_over_text, game_over_rect)
    surface.blit(score_text, score_rect)
    surface.blit(rank_text, rank_rect)
    surface.blit(instruction_text, instruction_rect)

def reset_game():
    """Reinicia o estado do jogo para começar de novo."""
    global score, game_state, player
    
    score = 0
    game_state = 'playing'
    
    # Limpa todos os sprites antigos
    all_sprites.empty()
    enemies_group.empty()
    bullets_group.empty()
    
    # Cria um novo jogador e o adiciona aos grupos
    player = Player(all_sprites, bullets_group)
    all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)

    if game_state == 'playing':
        # ##################################################
        # TODA A LÓGICA DO JOGO ATIVO VAI AQUI DENTRO
        # ##################################################
        
        # --- Processamento de Eventos (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == SPAWN_ENEMY_EVENT:
                enemy = Enemy(random.randrange(0, WIDTH - 40), -50)
                all_sprites.add(enemy)
                enemies_group.add(enemy)
            

        # --- Atualização da Lógica (Update) ---
        all_sprites.update()
        bg_distante.update()
        bg_estrelas.update()
        bg_proximo.update()
        
        # --- Verificação de Colisões ---
        hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True)
        for hit in hits:
            score += 10
            explosion_sound.play()
        
        player_hits = pygame.sprite.spritecollide(player, enemies_group, False)
        if player_hits:
            game_state = 'game_over'
            final_score = score

        # --- Desenho na Tela (Render) ---
        screen.fill(BLACK)
        bg_distante.draw(screen)
        bg_proximo.draw(screen)
        bg_estrelas.draw(screen)
        all_sprites.draw(screen)
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    elif game_state == 'game_over':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                reset_game()

        # Desenha a tela de Game Over
        screen.fill(BLACK)
        draw_game_over_screen(screen, final_score)


    # Esta linha executa sempre, não importa o estado, para mostrar as mudanças na tela
    pygame.display.flip()

# --- Fim do Jogo ---
pygame.quit()