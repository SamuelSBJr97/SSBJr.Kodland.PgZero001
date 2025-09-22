import importlib
import types

import pytest

from game import game


def test_imports_and_constants():
    # Deve importar sem lançar
    assert isinstance(game.WIDTH, int)
    assert isinstance(game.HEIGHT, int)


def test_init_and_get_counter():
    game.init()
    assert game.get_counter() == 0


def test_update_increments_counter():
    game.init()
    game.update(0.5)
    assert pytest.approx(game.get_counter(), rel=1e-6) == 0.5


def test_draw_does_not_raise():
    # Apenas garantir que draw pode ser chamado sem exceção
    game.init()
    game.draw()


def test_module_reload():
    # Recarregar módulo para garantir idempotência
    importlib.reload(game)
    game.init()
    game.update(1.0)
    assert pytest.approx(game.get_counter(), rel=1e-6) == 1.0
