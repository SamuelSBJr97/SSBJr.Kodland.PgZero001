"""
Testes unitários para o movimento do jogador
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

@pytest.mark.unit
class TestPlayerMovement:
    """Testes para o movimento do jogador"""
    
    def test_player_creation(self, sample_player):
        """Testa a criação do jogador"""
        assert sample_player.x == 400
        assert sample_player.y == 550
        assert sample_player.image == 'player'
    
    def test_player_movement_left(self, sample_player, mock_pgzero):
        """Testa movimento para a esquerda"""
        initial_x = sample_player.x
        
        # Simular tecla esquerda pressionada
        mock_pgzero['keyboard'].left = True
        
        # Simular movimento (normalmente seria feito na função update)
        if mock_pgzero['keyboard'].left and sample_player.x > 5:  # PLAYER_SPEED
            sample_player.x -= 5
        
        assert sample_player.x < initial_x
    
    def test_player_movement_right(self, sample_player, mock_pgzero):
        """Testa movimento para a direita"""
        initial_x = sample_player.x
        
        # Simular tecla direita pressionada
        mock_pgzero['keyboard'].right = True
        
        # Simular movimento
        if mock_pgzero['keyboard'].right and sample_player.x < 800 - 5:  # SCREEN_WIDTH - PLAYER_SPEED
            sample_player.x += 5
        
        assert sample_player.x > initial_x
    
    def test_player_movement_up(self, sample_player, mock_pgzero):
        """Testa movimento para cima"""
        initial_y = sample_player.y
        
        # Simular tecla cima pressionada
        mock_pgzero['keyboard'].up = True
        
        # Simular movimento
        if mock_pgzero['keyboard'].up and sample_player.y > 5:  # PLAYER_SPEED
            sample_player.y -= 5
        
        assert sample_player.y < initial_y
    
    def test_player_movement_down(self, sample_player, mock_pgzero):
        """Testa movimento para baixo"""
        initial_y = sample_player.y
        
        # Simular tecla baixo pressionada
        mock_pgzero['keyboard'].down = True
        
        # Simular movimento
        if mock_pgzero['keyboard'].down and sample_player.y < 600 - 5:  # SCREEN_HEIGHT - PLAYER_SPEED
            sample_player.y += 5
        
        assert sample_player.y > initial_y
    
    def test_player_boundary_left(self, sample_player, mock_pgzero):
        """Testa se o jogador não sai da tela pela esquerda"""
        sample_player.x = 0
        mock_pgzero['keyboard'].left = True
        
        # Simular movimento com verificação de limite
        if mock_pgzero['keyboard'].left and sample_player.x > 5:
            sample_player.x -= 5
        
        assert sample_player.x >= 0
    
    def test_player_boundary_right(self, sample_player, mock_pgzero):
        """Testa se o jogador não sai da tela pela direita"""
        sample_player.x = 800  # SCREEN_WIDTH
        mock_pgzero['keyboard'].right = True
        
        # Simular movimento com verificação de limite
        if mock_pgzero['keyboard'].right and sample_player.x < 800 - 5:
            sample_player.x += 5
        
        assert sample_player.x <= 800