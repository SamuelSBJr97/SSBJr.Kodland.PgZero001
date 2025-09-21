"""
Jogo Principal - PyGame Zero
Arquivo principal do jogo desenvolvido com PyGame Zero
"""

import pgzrun
from settings import *

# Variáveis globais do jogo
score = 0
game_over = False

# Criar atores/sprites
player = Actor('player', (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

# Lista para armazenar elementos do jogo
enemies = []
collectibles = []

def draw():
    """
    Função chamada automaticamente pelo PyGame Zero para desenhar na tela
    """
    # Limpar a tela com cor de fundo
    screen.fill(BACKGROUND_COLOR)
    
    if not game_over:
        # Desenhar o jogador
        player.draw()
        
        # Desenhar inimigos
        for enemy in enemies:
            enemy.draw()
        
        # Desenhar coletáveis
        for collectible in collectibles:
            collectible.draw()
        
        # Mostrar pontuação
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color="white")
        
        # Instruções
        screen.draw.text("Use as setas para mover", (10, SCREEN_HEIGHT - 60), fontsize=20, color="white")
        screen.draw.text("Pressione ESPAÇO para ação", (10, SCREEN_HEIGHT - 40), fontsize=20, color="white")
        screen.draw.text("Pressione ESC para sair", (10, SCREEN_HEIGHT - 20), fontsize=20, color="white")
    else:
        # Tela de game over
        screen.draw.text("GAME OVER", center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), fontsize=50, color="red")
        screen.draw.text(f"Pontuação Final: {score}", center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60), fontsize=30, color="white")
        screen.draw.text("Pressione R para reiniciar", center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100), fontsize=20, color="white")

def update():
    """
    Função chamada automaticamente pelo PyGame Zero para atualizar a lógica do jogo
    """
    global game_over
    
    if not game_over:
        # Movimentação do jogador
        if keyboard.left and player.x > PLAYER_SPEED:
            player.x -= PLAYER_SPEED
        if keyboard.right and player.x < SCREEN_WIDTH - PLAYER_SPEED:
            player.x += PLAYER_SPEED
        if keyboard.up and player.y > PLAYER_SPEED:
            player.y -= PLAYER_SPEED
        if keyboard.down and player.y < SCREEN_HEIGHT - PLAYER_SPEED:
            player.y += PLAYER_SPEED
        
        # Atualizar posição dos inimigos
        for enemy in enemies[:]:  # Usando slice para evitar problemas ao remover itens
            enemy.y += ENEMY_SPEED
            if enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)
            elif player.colliderect(enemy):
                game_over = True
        
        # Atualizar posição dos coletáveis
        for collectible in collectibles[:]:
            collectible.y += COLLECTIBLE_SPEED
            if collectible.y > SCREEN_HEIGHT:
                collectibles.remove(collectible)
            elif player.colliderect(collectible):
                global score
                score += 10
                collectibles.remove(collectible)

def on_key_down(key):
    """
    Função chamada quando uma tecla é pressionada
    """
    global game_over, score
    
    if key == keys.ESCAPE:
        exit()
    elif key == keys.SPACE and not game_over:
        # Ação principal do jogo (ex: atirar)
        pass
    elif key == keys.R and game_over:
        # Reiniciar o jogo
        game_over = False
        score = 0
        enemies.clear()
        collectibles.clear()
        player.pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

def spawn_enemy():
    """
    Função para criar novos inimigos
    """
    import random
    if not game_over and len(enemies) < MAX_ENEMIES:
        x = random.randint(50, SCREEN_WIDTH - 50)
        enemy = Actor('enemy', (x, -50))
        enemies.append(enemy)

def spawn_collectible():
    """
    Função para criar novos coletáveis
    """
    import random
    if not game_over and len(collectibles) < MAX_COLLECTIBLES:
        x = random.randint(50, SCREEN_WIDTH - 50)
        collectible = Actor('collectible', (x, -50))
        collectibles.append(collectible)

# Agendar a criação de inimigos e coletáveis
clock.schedule_interval(spawn_enemy, 2.0)  # Criar inimigo a cada 2 segundos
clock.schedule_interval(spawn_collectible, 3.0)  # Criar coletável a cada 3 segundos

# Inicializar o jogo
if __name__ == "__main__":
    pgzrun.go()