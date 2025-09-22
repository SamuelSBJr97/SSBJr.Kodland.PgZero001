from game.entities import Vector2, Player, create_default_player
from game.input import InputState


def test_player_move_zero():
    p = Player(pos=Vector2(0, 0), speed=100)
    p.move(0, 0, 1.0)
    assert p.pos.x == 0 and p.pos.y == 0


def test_player_move_direction():
    p = Player(pos=Vector2(0, 0), speed=10)
    p.move(1.0, 0.0, 0.5)
    assert p.pos.x == 5.0


def test_create_default_player_center():
    p = create_default_player()
    assert isinstance(p, Player)


def test_input_compute_direction():
    s = InputState()
    s.left = True
    dx, dy = s and __import__("game.input", fromlist=["compute_direction"]).compute_direction(s)
    # Apenas validar que retorna dois floats
    assert isinstance(dx, float) and isinstance(dy, float)
