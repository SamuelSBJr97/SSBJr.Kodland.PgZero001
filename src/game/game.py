"""Base mínima do jogo usando pgzero.

Este módulo fornece funções draw() e update() esperadas pelo pgzero.
Se pgzero não estiver instalado (por exemplo durante os testes), o módulo fornece um fallback que permite importar e chamar as funções sem erro.
"""

# Dimensões
WIDTH = 800
HEIGHT = 600

# Estado do jogo
_state = {
    "counter": 0,
}

# Tentativa de importar o objeto screen do pgzero; se não houver, criamos um stub simples.
try:
    import pgzrun  # noqa: F401
    from pgzero.builtins import Actor
    from pgzero import screen
    _HAS_PGZERO = True
except Exception:
    # Fallback stub
    class _DummyScreen:
        def clear(self):
            pass

        def draw(self, *args, **kwargs):
            pass

    screen = _DummyScreen()
    Actor = object
    _HAS_PGZERO = False


def init():
    """Inicializa ou reseta o estado do jogo."""
    _state["counter"] = 0


def update(dt=1.0):
    """Atualiza o estado do jogo.

    Parâmetros:
    - dt: delta time em segundos (opcional, usado para testes)
    """
    # Incrementa o contador em função do tempo
    _state["counter"] += dt


def draw():
    """Desenha o estado atual. Usa screen se disponível.

    Deve ser chamada por pgzero. Em testes simplesmente não lança erro.
    """
    # Chamada segura a um possível método de limpeza do screen (nem todas as
    # versões de pgzero expõem screen.clear()). Se não existir, não faz nada.
    try:
        clear_fn = getattr(screen, "clear", None)
        if callable(clear_fn):
            clear_fn()
    except Exception:
        # Nunca deixar uma falha no desenho quebrar os testes.
        pass

    # Em pgzero real, usar screen.draw.text etc. Aqui apenas um stub seguro.
    try:
        draw_obj = getattr(screen, "draw", None)
        if draw_obj is not None:
            # exemplo: desenhar contador (não faz nada no stub)
            pass
    except Exception:
        pass


def get_counter():
    """Retorna o valor atual do contador para os testes."""
    return _state["counter"]
