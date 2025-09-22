"""Entrada/controles - interface leve para testes."""


class InputState:
    """Representa estado simplificado das teclas direcionais."""

    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    def reset(self):
        self.left = self.right = self.up = self.down = False


def compute_direction(state: InputState):
    dx = 0.0
    dy = 0.0
    if state.left:
        dx -= 1.0
    if state.right:
        dx += 1.0
    if state.up:
        dy -= 1.0
    if state.down:
        dy += 1.0
    return dx, dy
