"""Versão jogável com Pygame Zero: desenha salas, player, colisão e perguntas MCQ."""

from .settings import WIDTH, HEIGHT, FPS, DEFAULT_SEED, DEFAULT_NUM_ROOMS
from .mapgen import generate_map
from .questions import sample_questions
from .book import default_books_for_room
import random

_HAS_PGZERO = True
try:
    from pgzero.builtins import Actor
    from pgzero import screen
    from pgzero.keyboard import keys
except Exception:
    _HAS_PGZERO = False
    class Actor:
        def __init__(self, *args, **kwargs):
            self.x = 0
            self.y = 0

    class _DummyScreen:
        def clear(self):
            pass
        def draw(self, *a, **k):
            pass

    screen = _DummyScreen()
    class keys:
        LEFT = 'left'
        RIGHT = 'right'
        UP = 'up'
        DOWN = 'down'
        K_1 = '1'
        K_2 = '2'
        K_3 = '3'


TITLE = "Mapa das Charadas"


class Game:
    def __init__(self, seed=None, num_rooms=None):
        if seed is None:
            seed = DEFAULT_SEED
        if num_rooms is None:
            num_rooms = DEFAULT_NUM_ROOMS
        self.seed = seed
        self.rng = random.Random(seed)
        self.map = generate_map(seed, num_rooms=num_rooms)
        # simple player
        self.player = Actor('player') if _HAS_PGZERO else Actor()
        self.player.x = WIDTH // 2
        self.player.y = HEIGHT // 2
        self.speed = 180
        self.in_question = False
        self.current_room = None
        self.books = []
        self.questions = []
        self.choices = []
        self.selected = []
        self.score = 0

    def move(self, dx, dy, dt):
        self.player.x += dx * self.speed * dt
        self.player.y += dy * self.speed * dt

    def check_room_collision(self):
        # retorna index da sala onde o centro do player está
        px, py = int(self.player.x), int(self.player.y)
        for r in self.map.rooms:
            if r.x <= px <= r.x + r.w and r.y <= py <= r.y + r.h:
                return r
        return None

    def enter_room(self, room):
        if room is None:
            return False
        if self.score < room.required_score:
            return False
        self.current_room = room
        # carregar livros e perguntas
        self.books = default_books_for_room(room.id)
        qs = sample_questions(room.theme, self.rng, count=3)
        self.questions = qs
        self.choices = [q.get('choices', []) for q in qs]
        self.selected = [None] * len(qs)
        self.in_question = True
        return True

    def answer_current(self, q_index, choice_index):
        if not self.in_question:
            return
        self.selected[q_index] = choice_index
        # if all answered, evaluate
        if all(x is not None for x in self.selected):
            correct = 0
            for i, q in enumerate(self.questions):
                chosen = self.choices[i][self.selected[i]]
                if str(chosen).strip().lower() == str(q['answer']).strip().lower():
                    correct += 1
            if correct == len(self.questions):
                pts = sum(q.get('difficulty', 1) for q in self.questions)
                self.score += pts
                # unlock books
                for b in self.books:
                    b.locked = False
            # exit question mode
            self.in_question = False


G = Game()


def update(dt):
    # handle movement keys reading from keyboard via pgzero (not available in tests)
    if G.in_question:
        return
    # movement handled via on_key_down for simplicity (instant moves)
    pass


def draw():
    try:
        clear_fn = getattr(screen, 'clear', None)
        if callable(clear_fn):
            clear_fn()
    except Exception:
        pass
    # draw rooms
    try:
        for r in G.map.rooms:
            screen.draw.rect((r.x, r.y, r.w, r.h), 'gray')
        # draw player
        screen.draw.filled_circle((int(G.player.x), int(G.player.y)), 8, 'blue')
        # HUD
        screen.draw.text(f"Score: {G.score}", (10, 10))
        if G.in_question:
            y = 60
            for i, q in enumerate(G.questions):
                screen.draw.text(f"{i+1}. {q['question']}", (20, y))
                y += 24
                for j, c in enumerate(G.choices[i]):
                    screen.draw.text(f"{j+1}) {c}", (40, y))
                    y += 20
                y += 10
    except Exception:
        pass


def on_key_down(key):
    # movement
    if not G.in_question:
        if key == keys.LEFT:
            G.move(-1, 0, 1/60)
        elif key == keys.RIGHT:
            G.move(1, 0, 1/60)
        elif key == keys.UP:
            G.move(0, -1, 1/60)
        elif key == keys.DOWN:
            G.move(0, 1, 1/60)
        elif key == keys.K_1:
            room = G.check_room_collision()
            if room:
                G.enter_room(room)
    else:
        # answer first unanswered question with key 1/2/3
        if key == keys.K_1:
            # answer question 0 choice 0 if available
            for idx in range(len(G.selected)):
                if G.selected[idx] is None:
                    if len(G.choices[idx]) > 0:
                        G.answer_current(idx, 0)
                    break
        elif key == keys.K_2:
            for idx in range(len(G.selected)):
                if G.selected[idx] is None:
                    if len(G.choices[idx]) > 1:
                        G.answer_current(idx, 1)
                    break
        elif key == keys.K_3:
            for idx in range(len(G.selected)):
                if G.selected[idx] is None:
                    if len(G.choices[idx]) > 2:
                        G.answer_current(idx, 2)
                    break
"""Implementação do jogo visual usando Pygame Zero (pgzero).

Este módulo define as funções e variáveis esperadas pelo pgzrun: WIDTH, HEIGHT,
update(), draw(), on_key_down() e usa Actors para o player.

O arquivo é protegido para permitir import sem pgzero (ex.: testes).
"""

from .settings import WIDTH, HEIGHT
from .mapgen import generate_map
from .settings import DEFAULT_SEED, DEFAULT_NUM_ROOMS
from .questions import sample_questions
import random

_HAS_PGZERO = True
try:
    from pgzero.builtins import Actor
    from pgzero import screen
    from pgzero.keyboard import keys
except Exception:
    # stubs para permitir import sem pgzero
    _HAS_PGZERO = False

    class Actor:
        def __init__(self, *args, **kwargs):
            self.x = 0
            self.y = 0

    class _DummyScreen:
        def clear(self):
            pass

        def draw(self, *a, **k):
            pass

    screen = _DummyScreen()
    class keys:
        LEFT = 'left'
        RIGHT = 'right'
        UP = 'up'
        DOWN = 'down'
        K_1 = '1'
        K_2 = '2'
        K_3 = '3'


# Estado do jogo visual
class VisualGame:
    def __init__(self, seed: int = None, num_rooms: int = None):
        if seed is None:
            seed = DEFAULT_SEED
        if num_rooms is None:
            num_rooms = DEFAULT_NUM_ROOMS
        self.seed = seed
        self.num_rooms = num_rooms
        self.rng = random.Random(seed)
        self.map = generate_map(seed, num_rooms=num_rooms)
        # player actor
        self.player = Actor('player') if _HAS_PGZERO else Actor()
        self.player.x = WIDTH // 2
        self.player.y = HEIGHT // 2
        self.speed = 200
        self.current_room = None
        self.in_question = False
        self.current_questions = []
        self.current_choices = []
        self.correct_answer = None
        self.selected_choice = None
        self.player_score = 0

    def move_player(self, dx, dy, dt):
        self.player.x += dx * self.speed * dt
        self.player.y += dy * self.speed * dt

    def try_enter_room_under_player(self):
        # Implementação protótipo: entrar em room 0 quando player perto do centro
        if abs(self.player.x - WIDTH // 2) < 20 and abs(self.player.y - HEIGHT // 2) < 20:
            self.current_room = self.map.rooms[0]
            return True
        return False

    def start_questions_for_room(self):
        if not self.current_room:
            return
        theme = getattr(self.current_room, 'theme', None)
        if theme is None:
            return
        qs = sample_questions(theme, self.rng, count=3, min_difficulty=1)
        if len(qs) < 3:
            return
        self.current_questions = qs
        # save choices and correct
        self.current_choices = [q.get('choices', []) for q in qs]
        self.correct_answer = [str(q.get('answer')).strip().lower() for q in qs]
        self.in_question = True
        self.selected_choice = [None] * len(qs)


VG = VisualGame()

# API esperada pelo pgzero
def update(dt):
    # nothing complex; movement via on_key_down
    if VG.in_question:
        return


def draw():
    # clear
    try:
        clear_fn = getattr(screen, 'clear', None)
        if callable(clear_fn):
            clear_fn()
    except Exception:
        pass

    # Draw tile map using floor image for all tiles and wall for room borders if available
    try:
        # prefer to use Actor image surfaces if available
        has_images = _HAS_PGZERO
        # tile size (we used 64x64 floor)
        tile_w, tile_h = 64, 64
        # draw a tiled background
        for x in range(0, WIDTH, tile_w):
            for y in range(0, HEIGHT, tile_h):
                try:
                    if has_images:
                        screen.blit('floor', (x, y))
                    else:
                        screen.draw.filled_rect((x, y, tile_w, tile_h), (200, 200, 200))
                except Exception:
                    screen.draw.filled_rect((x, y, tile_w, tile_h), (200, 200, 200))

        # draw rooms as walls or rect outlines
        for r in VG.map.rooms:
            try:
                # draw interior as slightly darker
                screen.draw.filled_rect((r.x, r.y, r.w, r.h), (170, 170, 170))
                # border
                if has_images:
                    # draw wall image at room edges (approximation)
                    screen.blit('wall', (r.x, r.y))
                else:
                    screen.draw.rect((r.x, r.y, r.w, r.h), 'black')
            except Exception:
                try:
                    screen.draw.rect((r.x, r.y, r.w, r.h), 'black')
                except Exception:
                    pass

        # draw player (Actor when available)
        try:
            if _HAS_PGZERO:
                # Actor knows how to draw itself via screen.blit internal to pgzero
                Gx, Gy = int(VG.player.x), int(VG.player.y)
                screen.blit('player', (Gx - 16, Gy - 16))
            else:
                screen.draw.filled_circle((int(VG.player.x), int(VG.player.y)), 8, 'blue')
        except Exception:
            try:
                screen.draw.filled_circle((int(VG.player.x), int(VG.player.y)), 8, 'blue')
            except Exception:
                pass

        # HUD
        try:
            screen.draw.text(f"Score: {VG.player_score}", (10, 10))
        except Exception:
            pass
    except Exception:
        # last-resort fallback: simple shapes
        try:
            for r in VG.map.rooms:
                screen.draw.rect((r.x, r.y, r.w, r.h), 'gray')
            screen.draw.filled_circle((int(VG.player.x), int(VG.player.y)), 8, 'blue')
        except Exception:
            pass


def on_key_down(key):
    # movement via arrow keys
    if VG.in_question:
        # existing question handling
        if key == keys.K_1:
            sel = 0
        elif key == keys.K_2:
            sel = 1
        elif key == keys.K_3:
            sel = 2
        else:
            sel = None
        if sel is not None:
            VG.selected_choice[0] = sel
            if all(x is not None for x in VG.selected_choice):
                correct = 0
                for i, q in enumerate(VG.current_questions):
                    choice_text = VG.current_choices[i][VG.selected_choice[i]]
                    if choice_text.strip().lower() == str(q['answer']).strip().lower():
                        correct += 1
                if correct == len(VG.current_questions):
                    VG.player_score += sum(q.get('difficulty', 1) for q in VG.current_questions)
                VG.in_question = False
    else:
        if key == keys.LEFT:
            VG.move_player(-1, 0, 0.016)
        elif key == keys.RIGHT:
            VG.move_player(1, 0, 0.016)
        elif key == keys.UP:
            VG.move_player(0, -1, 0.016)
        elif key == keys.DOWN:
            VG.move_player(0, 1, 0.016)
        elif key == keys.K_1:
            if VG.try_enter_room_under_player():
                VG.start_questions_for_room()