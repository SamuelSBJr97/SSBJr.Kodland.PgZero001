"""Entidades simples para o jogo - versão testável sem dependência de pgzero."""
from dataclasses import dataclass
from .settings import WIDTH, HEIGHT


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0


@dataclass
class Player:
    pos: Vector2
    speed: float = 200.0  # pixels por segundo

    def move(self, dx: float, dy: float, dt: float):
        """Mover o jogador por dx/dy (normalizado) multiplicado por speed e dt."""
        self.pos.x += dx * self.speed * dt
        self.pos.y += dy * self.speed * dt


def create_default_player():
    return Player(pos=Vector2(x=WIDTH / 2, y=HEIGHT / 2))
