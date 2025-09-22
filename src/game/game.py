"""Implementação do jogo com menu, geração de mapa e salas.

Este módulo também expõe uma API compatível com a versão inicial usada nos
testes: `WIDTH`, `HEIGHT`, `init()`, `update(dt)`, `draw()` e `get_counter()`.
As partes de jogo (mapa, salas, perguntas) permanecem disponíveis na mesma
module API para desenvolvimento posterior.
"""

from .settings import WIDTH, HEIGHT, DEFAULT_SEED, DEFAULT_NUM_ROOMS

from .ui import MENU, DESCRIPTION, format_menu
from .mapgen import generate_map
from .room import Room
from .questions import sample_questions
import random

# Estado simplificado do jogo
class GameState:
    def __init__(self):
        self.mode = "menu"  # menu, playing
        self.selected_menu = 0
        self.seed = DEFAULT_SEED
        self.map = None
        self.current_room = None
        self.player_score = 0
        self.rng = random.Random(self.seed)

    def start_game(self, seed: int = None, num_rooms: int = None):
        # usa seed padrão de settings se não informado
        if seed is not None:
            self.seed = seed
        if num_rooms is None:
            num_rooms = DEFAULT_NUM_ROOMS
        self.map = generate_map(self.seed, num_rooms=num_rooms)
        self.mode = "playing"
        self.player_score = 0

    def goto_room(self, room_id: int):
        desc = next((r for r in self.map.rooms if r.id == room_id), None)
        if desc is None:
            raise ValueError("Sala desconhecida")
        self.current_room = Room(desc)


_GS = GameState()


def menu_text():
    return format_menu(_GS.selected_menu) + "\n\n" + DESCRIPTION


def toggle_sound():
    # stub: alterna um estado que poderia controlar som
    return True


def enter_room(room_id: int):
    """Tenta entrar em uma sala: retorna (can_enter, info)"""
    if _GS.map is None:
        return False, None
    desc = next((r for r in _GS.map.rooms if r.id == room_id), None)
    if desc is None:
        return False, None
    can = _GS.player_score >= desc.required_score
    return can, desc


def ask_room_questions(theme: str, answers: list):
    """Pega 3 perguntas do tema (respeitando min difficulty) e compara com respostas.

    Retorna (success: bool, correct_count: int, total_points: int, details)
    """
    qs = sample_questions(theme, _GS.rng, count=3, min_difficulty=1)
    # se não há perguntas suficientes, falha
    if len(qs) < 3:
        return False, 0, 0, qs
    room = _GS.current_room
    if room is None:
        # tentativa automática: escolher a primeira sala do mapa, se existir
        if _GS.map and len(_GS.map.rooms) > 0:
            _GS.goto_room(_GS.map.rooms[0].id)
            room = _GS.current_room
        else:
            return False, 0, 0, qs
    success = room.ask_questions(qs, answers)
    if success:
        pts = sum(q.get("difficulty", 1) for q in qs)
        _GS.player_score += pts
        return True, 3, pts, qs
    else:
        # falhou -> reinicia estado da sala sem pontos
        return False, 0, 0, qs


def get_state_snapshot():
    return {
        "mode": _GS.mode,
        "seed": _GS.seed,
        "num_rooms": _GS.map.num_rooms if _GS.map else 0,
        "player_score": _GS.player_score,
    }


# Test helpers
def reset_for_tests():
    # Reseta o objeto global existente para preservar referências importadas
    _GS.mode = "menu"
    _GS.selected_menu = 0
    _GS.seed = 42
    _GS.map = None
    _GS.current_room = None
    _GS.player_score = 0
    _GS.rng = random.Random(_GS.seed)
    return _GS


# --- Compat API simples (antigos testes) ---------------------------------
_counter = 0.0


def init():
    global _counter
    _counter = 0.0


def update(dt=1.0):
    global _counter
    _counter += dt


def draw():
    # stub para compatibilidade: nada a desenhar nos testes
    return None


def get_counter():
    return _counter

