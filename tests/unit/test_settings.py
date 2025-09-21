"""
Testes unitários para as configurações do jogo
"""

import pytest
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from settings import *

@pytest.mark.unit
class TestSettings:
    """Testes para as configurações do jogo"""
    
    def test_screen_dimensions(self):
        """Testa se as dimensões da tela estão corretas"""
        assert SCREEN_WIDTH > 0
        assert SCREEN_HEIGHT > 0
        assert isinstance(SCREEN_WIDTH, int)
        assert isinstance(SCREEN_HEIGHT, int)
    
    def test_colors_format(self):
        """Testa se as cores estão no formato RGB correto"""
        def is_valid_rgb(color):
            return (isinstance(color, tuple) and 
                   len(color) == 3 and 
                   all(0 <= c <= 255 for c in color))
        
        assert is_valid_rgb(BACKGROUND_COLOR)
        assert is_valid_rgb(WHITE)
        assert is_valid_rgb(BLACK)
        assert is_valid_rgb(RED)
        assert is_valid_rgb(GREEN)
        assert is_valid_rgb(BLUE)
        assert is_valid_rgb(YELLOW)
    
    def test_speed_values(self):
        """Testa se os valores de velocidade são positivos"""
        assert PLAYER_SPEED > 0
        assert ENEMY_SPEED > 0
        assert COLLECTIBLE_SPEED > 0
        assert isinstance(PLAYER_SPEED, (int, float))
        assert isinstance(ENEMY_SPEED, (int, float))
        assert isinstance(COLLECTIBLE_SPEED, (int, float))
    
    def test_max_entities(self):
        """Testa se os valores máximos de entidades são válidos"""
        assert MAX_ENEMIES > 0
        assert MAX_COLLECTIBLES > 0
        assert isinstance(MAX_ENEMIES, int)
        assert isinstance(MAX_COLLECTIBLES, int)
    
    def test_volume_settings(self):
        """Testa se as configurações de volume estão no range correto"""
        assert 0.0 <= MUSIC_VOLUME <= 1.0
        assert 0.0 <= SOUND_VOLUME <= 1.0
    
    def test_fps_setting(self):
        """Testa se a configuração de FPS é válida"""
        assert FPS > 0
        assert isinstance(FPS, int)