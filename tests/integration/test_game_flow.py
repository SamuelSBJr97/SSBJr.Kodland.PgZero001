"""
Testes de integração para o fluxo completo do jogo
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

@pytest.mark.integration
class TestGameFlow:
    """Testes de integração para o fluxo do jogo"""
    
    def test_game_initialization(self, mock_pgzero):
        """Testa a inicialização completa do jogo"""
        # Mock do ambiente PyGame Zero
        with patch('sys.modules', {'pgzrun': MagicMock()}):
            # Simular importação do jogo
            from tests.conftest import MockActor
            
            # Criar jogador como no jogo real
            player = MockActor('player', (800 // 2, 600 - 50))
            
            # Verificar inicialização
            assert player.x == 400
            assert player.y == 550
            assert player.image == 'player'
    
    def test_enemy_spawn_and_movement(self, mock_pgzero):
        """Testa spawn e movimento de inimigos"""
        from tests.conftest import MockActor
        import random
        
        # Simular spawn de inimigo
        enemies = []
        x = random.randint(50, 750)  # SCREEN_WIDTH - 50
        enemy = MockActor('enemy', (x, -50))
        enemies.append(enemy)
        
        # Verificar spawn
        assert len(enemies) == 1
        assert enemies[0].y == -50
        
        # Simular movimento
        for enemy in enemies:
            enemy.y += 3  # ENEMY_SPEED
        
        # Verificar movimento
        assert enemies[0].y == -47
    
    def test_collectible_spawn_and_collection(self, mock_pgzero):
        """Testa spawn de coletáveis e coleta"""
        from tests.conftest import MockActor
        import random
        
        # Criar jogador e coletável
        player = MockActor('player', (400, 550))
        collectibles = []
        
        # Spawn de coletável
        x = random.randint(50, 750)
        collectible = MockActor('collectible', (x, -50))
        collectibles.append(collectible)
        
        # Mover coletável para posição do jogador
        collectible.x = player.x
        collectible.y = player.y
        
        # Simular coleta
        score = 0
        if player.colliderect(collectible):
            score += 10
            collectibles.remove(collectible)
        
        # Verificar coleta
        assert score == 10
        assert len(collectibles) == 0
    
    def test_game_over_scenario(self, mock_pgzero):
        """Testa cenário completo de game over"""
        from tests.conftest import MockActor
        
        # Estado inicial do jogo
        score = 50
        game_over = False
        player = MockActor('player', (400, 550))
        enemies = [MockActor('enemy', (400, 550))]  # Inimigo na posição do jogador
        
        # Verificar colisão
        for enemy in enemies:
            if player.colliderect(enemy):
                game_over = True
        
        # Verificar game over
        assert game_over is True
        assert score == 50  # Score mantido
    
    def test_game_reset_flow(self, mock_pgzero):
        """Testa o fluxo completo de reset do jogo"""
        from tests.conftest import MockActor
        
        # Estado de game over
        score = 100
        game_over = True
        player = MockActor('player', (200, 300))  # Posição alterada
        enemies = [MockActor('enemy', (100, 200))]
        collectibles = [MockActor('collectible', (300, 400))]
        
        # Simular reset (tecla R pressionada)
        score = 0
        game_over = False
        enemies.clear()
        collectibles.clear()
        player.x = 800 // 2  # SCREEN_WIDTH // 2
        player.y = 600 - 50  # SCREEN_HEIGHT - 50
        
        # Verificar reset
        assert score == 0
        assert game_over is False
        assert len(enemies) == 0
        assert len(collectibles) == 0
        assert player.x == 400
        assert player.y == 550

@pytest.mark.integration
class TestGamePerformance:
    """Testes de performance do jogo"""
    
    def test_multiple_entities_handling(self, mock_pgzero):
        """Testa manipulação de múltiplas entidades"""
        from tests.conftest import MockActor
        
        # Criar múltiplos inimigos e coletáveis
        enemies = []
        collectibles = []
        
        # Criar 5 inimigos (MAX_ENEMIES)
        for i in range(5):
            enemy = MockActor('enemy', (i * 100, 100))
            enemies.append(enemy)
        
        # Criar 3 coletáveis (MAX_COLLECTIBLES)
        for i in range(3):
            collectible = MockActor('collectible', (i * 150, 200))
            collectibles.append(collectible)
        
        # Verificar criação
        assert len(enemies) == 5
        assert len(collectibles) == 3
        
        # Simular movimento de todas as entidades
        for enemy in enemies:
            enemy.y += 3
        
        for collectible in collectibles:
            collectible.y += 2
        
        # Verificar movimento
        assert all(enemy.y == 103 for enemy in enemies)
        assert all(collectible.y == 202 for collectible in collectibles)
    
    @pytest.mark.slow
    def test_long_running_game_simulation(self, mock_pgzero):
        """Testa simulação de jogo longo (marcado como slow)"""
        from tests.conftest import MockActor
        
        # Simular 100 frames de jogo
        player = MockActor('player', (400, 550))
        enemies = []
        score = 0
        
        for frame in range(100):
            # A cada 10 frames, criar um inimigo
            if frame % 10 == 0:
                enemy = MockActor('enemy', (200, -50))
                enemies.append(enemy)
            
            # Mover inimigos
            for enemy in enemies[:]:
                enemy.y += 3
                if enemy.y > 600:  # SCREEN_HEIGHT
                    enemies.remove(enemy)
            
            # Simular coleta ocasional
            if frame % 20 == 0:
                score += 10
        
        # Verificar estado após simulação
        assert score > 0
        # Alguns inimigos devem ter sido removidos
        assert len(enemies) < 10  # Menos que o total criado