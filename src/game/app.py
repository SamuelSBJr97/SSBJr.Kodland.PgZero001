"""Aplicação principal do jogo — integra entidades, input e resources.

Projetado para ser importável em testes sem depender de pgzero em import.
"""
from .settings import WIDTH, HEIGHT
from .entities import create_default_player
from .input import InputState, compute_direction


class GameApp:
    def __init__(self):
        self.player = create_default_player()
        self.input = InputState()

    def init(self):
        self.player = create_default_player()
        self.input.reset()

    def update(self, dt: float):
        dx, dy = compute_direction(self.input)
        self.player.move(dx, dy, dt)

    def draw(self):
        # No-op para testes; em runtime, usaria screen.draw
        pass


def create_app():
    return GameApp()
