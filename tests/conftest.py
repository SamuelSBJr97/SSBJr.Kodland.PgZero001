"""
Configurações e fixtures para os testes do projeto PyGame Zero
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Adicionar o diretório src ao path para importar os módulos do jogo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock do pygame e pgzero para testes
class MockActor:
    """Mock da classe Actor do PyGame Zero"""
    def __init__(self, image, pos):
        self.image = image
        self.x, self.y = pos
        self.pos = pos
        
    def colliderect(self, other):
        """Mock simples de detecção de colisão"""
        return (abs(self.x - other.x) < 50 and 
                abs(self.y - other.y) < 50)
    
    def draw(self):
        """Mock do método draw"""
        pass

class MockScreen:
    """Mock da tela do PyGame Zero"""
    def __init__(self):
        self.width = 800
        self.height = 600
        
    def fill(self, color):
        """Mock do preenchimento da tela"""
        pass
    
    class draw:
        @staticmethod
        def text(text, pos=None, center=None, fontsize=30, color="white"):
            """Mock do desenho de texto"""
            pass

class MockKeyboard:
    """Mock do teclado do PyGame Zero"""
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

class MockClock:
    """Mock do clock do PyGame Zero"""
    @staticmethod
    def schedule_interval(func, interval):
        """Mock do agendamento de funções"""
        pass

# Fixtures para os testes
@pytest.fixture
def mock_pgzero(monkeypatch):
    """
    Fixture que mocka os componentes principais do PyGame Zero
    """
    # Mock das classes principais
    monkeypatch.setattr('builtins.Actor', MockActor)
    
    # Mock dos objetos globais
    mock_screen = MockScreen()
    mock_keyboard = MockKeyboard()
    mock_clock = MockClock()
    
    # Aplicar os mocks
    monkeypatch.setattr('builtins.screen', mock_screen)
    monkeypatch.setattr('builtins.keyboard', mock_keyboard)
    monkeypatch.setattr('builtins.clock', mock_clock)
    
    # Mock do keys para testes de teclado
    class MockKeys:
        ESCAPE = 'escape'
        SPACE = 'space'
        R = 'r'
    
    monkeypatch.setattr('builtins.keys', MockKeys())
    
    return {
        'screen': mock_screen,
        'keyboard': mock_keyboard,
        'clock': mock_clock,
        'Actor': MockActor
    }

@pytest.fixture
def game_state():
    """
    Fixture que fornece um estado inicial do jogo para testes
    """
    return {
        'score': 0,
        'game_over': False,
        'player_pos': (400, 550),
        'enemies': [],
        'collectibles': []
    }

@pytest.fixture
def sample_player():
    """
    Fixture que cria um jogador de exemplo para testes
    """
    return MockActor('player', (400, 550))

@pytest.fixture
def sample_enemy():
    """
    Fixture que cria um inimigo de exemplo para testes
    """
    return MockActor('enemy', (200, 100))

@pytest.fixture
def sample_collectible():
    """
    Fixture que cria um coletável de exemplo para testes
    """
    return MockActor('collectible', (300, 150))

# Configurações do pytest
def pytest_configure(config):
    """
    Configurações personalizadas do pytest
    """
    # Configurar marcadores personalizados
    config.addinivalue_line(
        "markers", 
        "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", 
        "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", 
        "slow: marca testes que demoram para executar"
    )

# Função auxiliar para configurar o ambiente de teste
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """
    Configuração automática do ambiente de teste
    """
    # Desabilitar saída de áudio durante os testes
    monkeypatch.setenv('SDL_AUDIODRIVER', 'dummy')
    
    # Configurar display dummy para testes sem interface gráfica
    monkeypatch.setenv('SDL_VIDEODRIVER', 'dummy')