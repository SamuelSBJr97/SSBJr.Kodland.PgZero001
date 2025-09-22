"""UI e menu básico para o jogo (sem dependência direta de pgzero no import).

Contém strings e helpers para montar a tela de menu com: começar, som, sair e explicação.
"""

MENU = {
    "title": "Mapa das Charadas",
    "options": ["Começar Jogo", "Controle de Som", "Sair"],
}

DESCRIPTION = (
    "Neste jogo você explora mapas gerados por seed. Cada mapa contém salas com desafios de matemática, lógica e Python. "
    "Em cada sala um guardião fará 3 perguntas. Responda corretamente para ganhar os pontos da sala. "
    "Use livros nas salas e corredores para estudar a teoria necessária antes de tentar as charadas."
)


def format_menu(selected: int = 0):
    lines = [MENU["title"], ""]
    for i, opt in enumerate(MENU["options"]):
        prefix = "> " if i == selected else "  "
        lines.append(prefix + opt)
    return "\n".join(lines)
