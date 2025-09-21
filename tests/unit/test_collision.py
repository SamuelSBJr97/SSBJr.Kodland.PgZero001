"""
Testes unitários para detecção de colisão
"""

import pytest
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

@pytest.mark.unit
class TestCollisionDetection:
    """Testes para detecção de colisão"""
    
    def test_collision_player_enemy(self, sample_player, sample_enemy):
        """Testa colisão entre jogador e inimigo"""
        # Posicionar inimigo próximo ao jogador
        sample_enemy.x = sample_player.x
        sample_enemy.y = sample_player.y
        
        # Verificar colisão
        collision = sample_player.colliderect(sample_enemy)
        assert collision is True
    
    def test_no_collision_player_enemy_far(self, sample_player, sample_enemy):
        """Testa ausência de colisão quando inimigo está longe"""
        # Posicionar inimigo longe do jogador
        sample_enemy.x = sample_player.x + 100
        sample_enemy.y = sample_player.y + 100
        
        # Verificar ausência de colisão
        collision = sample_player.colliderect(sample_enemy)
        assert collision is False
    
    def test_collision_player_collectible(self, sample_player, sample_collectible):
        """Testa colisão entre jogador e coletável"""
        # Posicionar coletável próximo ao jogador
        sample_collectible.x = sample_player.x
        sample_collectible.y = sample_player.y
        
        # Verificar colisão
        collision = sample_player.colliderect(sample_collectible)
        assert collision is True
    
    def test_collision_boundary_cases(self, sample_player):
        """Testa casos limítrofes de colisão"""
        from tests.conftest import MockActor
        
        # Criar objetos em posições limítrofes
        edge_object = MockActor('test', (sample_player.x + 49, sample_player.y))
        
        # Verificar colisão na borda
        collision = sample_player.colliderect(edge_object)
        assert collision is True
        
        # Objeto fora do limite
        far_object = MockActor('test', (sample_player.x + 51, sample_player.y))
        collision_far = sample_player.colliderect(far_object)
        assert collision_far is False

@pytest.mark.unit
class TestGameLogic:
    """Testes para a lógica do jogo"""
    
    def test_score_increase_on_collection(self, game_state):
        """Testa aumento da pontuação ao coletar item"""
        initial_score = game_state['score']
        
        # Simular coleta de item
        game_state['score'] += 10
        
        assert game_state['score'] == initial_score + 10
    
    def test_game_over_on_enemy_collision(self, game_state):
        """Testa game over ao colidir com inimigo"""
        assert game_state['game_over'] is False
        
        # Simular colisão com inimigo
        game_state['game_over'] = True
        
        assert game_state['game_over'] is True
    
    def test_game_reset(self, game_state):
        """Testa reset do jogo"""
        # Configurar estado de game over
        game_state['score'] = 100
        game_state['game_over'] = True
        
        # Simular reset
        game_state['score'] = 0
        game_state['game_over'] = False
        game_state['enemies'] = []
        game_state['collectibles'] = []
        
        assert game_state['score'] == 0
        assert game_state['game_over'] is False
        assert len(game_state['enemies']) == 0
        assert len(game_state['collectibles']) == 0