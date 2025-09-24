"""Standalone pygame runner to force a visible window and draw the map + player.

Use arrow keys to move. Loads images from src/game/images if available.
"""
import pgzero
import pygame
import random
from pathlib import Path
import sys
import textwrap
import json
from typing import Any

# pgzero keyboard/keys helpers (may be None when running without pgzero runner)
PGZ_KEYBOARD = getattr(pgzero, 'keyboard', None)
PGZ_KEYS = getattr(pgzero, 'keys', None)

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / 'src' / 'game' / 'images'

WIDTH, HEIGHT = 800, 600
FPS = 60

MAP_WIDTH, MAP_HEIGHT = 4000, 4000

def load_image(name, fallback_color=None, size=None):
    p = IMG_DIR / name
    if p.exists():
        try:
            im = pygame.image.load(str(p)).convert_alpha()
            if size:
                im = pygame.transform.scale(im, size)
            return im
        except Exception:
            pass
    # fallback: solid surface
    surf = pygame.Surface(size or (32, 32), pygame.SRCALPHA)
    surf.fill(fallback_color or (255, 0, 255))
    return surf


class Book:
    def __init__(self, x, y, text, points=1):
        self.x = x
        self.y = y
        self.w = 32
        self.h = 32
        self.text = text
        self.points = points
        self.read = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Guardian:
    def __init__(self, x, y, required_score=1, questions=None):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40
        self.required_score = required_score
        self.questions = questions or []
        self.defeated = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


def make_sample_questions():
    # simple MCQ: question dicts with 'question', 'choices', 'answer'
    return [
        {'question': 'Quanto é 2+2?', 'choices': ['3', '4', '5'], 'answer': '4'},
        {'question': 'Python: tipo de 1?','choices': ['str', 'int', 'list'], 'answer': 'int'},
        {'question': 'Lógica: True AND False =', 'choices': ['True','False','None'], 'answer': 'False'},
    ]

def load_questions_from_json():
    """Load questions from game.json file"""
    import json
    try:
        # file is located next to this module in the game package
        json_path = Path(__file__).resolve().parent / 'game.json'
        if not json_path.exists():
            # fallback: try relative to ROOT (src/game/game.json)
            json_path = ROOT / 'game' / 'game.json'
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'guardians' in data and len(data['guardians']) > 0:
                    return [guard.get('questions', make_sample_questions()) for guard in data['guardians']]
    except Exception as e:
        print(f'[error] failed to load questions from game.json: {e}')
    
    # fallback to sample questions
    return [make_sample_questions()]

# Global variable to store available question sets
QUESTION_SETS = []


# Game data loaded from game.json
GAME_BOOK_DEFS: dict[str, dict] = {}
GAME_GUARDIAN_DEFS: list[dict] = []
GAME_PLACEMENTS: dict = {}
BOOK_DEF_INDEX = 0
GUARDIAN_DEF_INDEX = 0
GAME_BOOK_LIST: list[dict] = []
PLACED_BOOK_IDS: set[str] = set()


def load_game_data():
    """Load full game data (books, guardians, placements) from game.json.
    Populates GAME_BOOK_DEFS, GAME_GUARDIAN_DEFS, GAME_PLACEMENTS.
    """
    global GAME_BOOK_DEFS, GAME_GUARDIAN_DEFS, GAME_PLACEMENTS
    GAME_BOOK_DEFS = {}
    GAME_GUARDIAN_DEFS = []
    GAME_PLACEMENTS = {}
    try:
        json_path = Path(__file__).resolve().parent / 'game.json'
        if not json_path.exists():
            json_path = ROOT / 'game' / 'game.json'
        if not json_path.exists():
            return
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # books (preserve order)
        GAME_BOOK_LIST = []
        for b in data.get('books', []) or []:
            if 'id' in b:
                GAME_BOOK_DEFS[b['id']] = b
                GAME_BOOK_LIST.append(b)
        # expose ordered list
        globals()['GAME_BOOK_LIST'] = GAME_BOOK_LIST
        # guardians
        GAME_GUARDIAN_DEFS = data.get('guardians', []) or []
        # placements
        GAME_PLACEMENTS = data.get('placements', {}) or {}
    except Exception as e:
        print(f'[error] load_game_data failed: {e}')


def place_book_in_room(r, book_def: dict | None = None):
    """Place a book inside room r, using book_def if provided or consuming next GAME_BOOK_LIST."""
    global BOOK_DEF_INDEX, GAME_BOOK_LIST, PLACED_BOOK_IDS
    margin = 15
    book_w, book_h = 32, 32
    if book_def is None:
        # find next unplaced book in GAME_BOOK_LIST
        while BOOK_DEF_INDEX < len(GAME_BOOK_LIST) and GAME_BOOK_LIST[BOOK_DEF_INDEX].get('id') in PLACED_BOOK_IDS:
            BOOK_DEF_INDEX += 1
        if BOOK_DEF_INDEX < len(GAME_BOOK_LIST):
            book_def = GAME_BOOK_LIST[BOOK_DEF_INDEX]
            BOOK_DEF_INDEX += 1
    if book_def:
        bx = r['x'] + margin + random.randint(0, max(0, r['w'] - 2*margin - book_w))
        by = r['y'] + margin + random.randint(0, max(0, r['h'] - 2*margin - book_h))
        books.append(Book(bx, by, text=book_def.get('text', 'Livro.'), points=book_def.get('points', 1)))
        PLACED_BOOK_IDS.add(book_def.get('id'))
    else:
        # fallback generic
        bx = r['x'] + margin + random.randint(0, max(0, r['w'] - 2*margin - book_w))
        by = r['y'] + margin + random.randint(0, max(0, r['h'] - 2*margin - book_h))
        books.append(Book(bx, by, text='Livro gerado na sala.', points=2))


def place_guardian_in_room(r, guardian_questions: list | None = None, guardian_required: int | None = None):
    """Place a guardian inside room r, using next GAME_GUARDIAN_DEFS or QUESTION_SETS as fallback."""
    global GUARDIAN_DEF_INDEX, GAME_GUARDIAN_DEFS, QUESTION_SETS
    guard_w, guard_h = 40, 40
    margin = 15
    gx = r['x'] + margin + random.randint(0, max(0, r['w'] - 2*margin - guard_w))
    gy = r['y'] + margin + random.randint(0, max(0, r['h'] - 2*margin - guard_h))
    if guardian_questions is None:
        if GUARDIAN_DEF_INDEX < len(GAME_GUARDIAN_DEFS):
            gdef = GAME_GUARDIAN_DEFS[GUARDIAN_DEF_INDEX]
            guardian_questions = gdef.get('questions', [])
            if guardian_required is None:
                guardian_required = gdef.get('required_score', 0)
            GUARDIAN_DEF_INDEX += 1
        else:
            if not QUESTION_SETS:
                QUESTION_SETS = load_questions_from_json()
            guardian_questions = QUESTION_SETS[ len(guardians) % max(1, len(QUESTION_SETS)) ]
    if guardian_required is None:
        guardian_required = 0
    guardians.append(Guardian(gx, gy, required_score=guardian_required, questions=guardian_questions))


# --- Converted to Pygame Zero style: module-level state + draw/update handlers ---


# occupancy grid settings (discrete cells for rooms to guarantee empty-adjacent placement)
GRID_CELL_W = 320
GRID_CELL_H = 240
GRID_MARGIN_X = 40
GRID_MARGIN_Y = 60
# set of occupied cells as (cx, cy)
occupied_cells = set()


# We'll keep most of the original logic but expose draw()/update()/on_key_down() for pgzero.
# To keep a consistent timestep we use a fixed dt based on FPS.
DT = 1.0 / FPS

# Game state (initialized by init_game)
rooms = []
books = []
guardians = []
px = WIDTH // 2
py = HEIGHT // 2
speed = 240
player_score = 0
show_completion = False
completion_timer = 0.0
mode = 'play'  # 'play', 'reading', 'guard_question', 'guard_question_results'
active_book = None
active_guardian = None
read_lines = []
scroll_y = 0
read_page = 0
font = None
big_font = None
g_questions: list[dict] = []
g_choices: list[list] = []
g_selected: list[int | None] = []
g_q_index = 0
g_results: list[bool | None] = []
result_timer = 0.0
floor = None
wall = None
player_img = None
book_img = None


def world_point_to_cell(x, y):
    cx = int((x - GRID_MARGIN_X) // GRID_CELL_W)
    cy = int((y - GRID_MARGIN_Y) // GRID_CELL_H)
    return cx, cy


def populate_room_with_book_guard(r, book_def: dict | None = None, guardian_questions: list | None = None, guardian_required: int | None = None):
    # reuse the logic from the original; ensure QUESTION_SETS loaded
    global QUESTION_SETS, BOOK_DEF_INDEX, GUARDIAN_DEF_INDEX, GAME_BOOK_DEFS
    margin = 15
    book_w, book_h = 32, 32
    guard_w, guard_h = 40, 40
    bx = r['x'] + 5
    by = r['y'] + 5
    gx = r['x'] + 5
    gy = r['y'] + 5
    min_width = 2*margin + max(book_w, guard_w) + 50
    min_height = 2*margin + max(book_h, guard_h)
    if r['w'] >= min_width and r['h'] >= min_height:
        bx = r['x'] + margin + random.randint(0, r['w'] - 2*margin - book_w)
        by = r['y'] + margin + random.randint(0, r['h'] - 2*margin - book_h)
        attempts = 0
        max_attempts = 20
        while attempts < max_attempts:
            gx = r['x'] + margin + random.randint(0, r['w'] - 2*margin - guard_w)
            gy = r['y'] + margin + random.randint(0, r['h'] - 2*margin - guard_h)
            book_rect = pygame.Rect(bx - 5, by - 5, book_w + 10, book_h + 10)
            guard_rect = pygame.Rect(gx, gy, guard_w, guard_h)
            if not book_rect.colliderect(guard_rect):
                break
            attempts += 1
        if attempts >= max_attempts:
            bx = r['x'] + margin
            by = r['y'] + margin
            gx = r['x'] + r['w'] - margin - guard_w
            gy = r['y'] + r['h'] - margin - guard_h
    else:
        bx = r['x'] + 5
        by = r['y'] + 5
        gx = r['x'] + r['w'] - guard_w - 5
        gy = r['y'] + r['h'] - guard_h - 5
        gx = max(r['x'] + 5, min(gx, r['x'] + r['w'] - guard_w - 5))
        gy = max(r['y'] + 5, min(gy, r['y'] + r['h'] - guard_h - 5))
    # create book using provided definition if available, else consume next GAME_BOOK_DEFS
    b_text = 'Livro gerado na sala.'
    b_points = 2
    if book_def is None:
        # pick next book def if available
        keys = list(GAME_BOOK_DEFS.keys())
        if BOOK_DEF_INDEX < len(keys):
            book_def = GAME_BOOK_DEFS[keys[BOOK_DEF_INDEX]]
            BOOK_DEF_INDEX += 1
    if book_def:
        b_text = book_def.get('text', b_text)
        b_points = book_def.get('points', b_points)
    books.append(Book(bx, by, text=b_text, points=b_points))
    # ensure questions for guardian
    if guardian_questions is None:
        # prefer guardian defs from GAME_GUARDIAN_DEFS if available
        if GUARDIAN_DEF_INDEX < len(GAME_GUARDIAN_DEFS):
            gdef = GAME_GUARDIAN_DEFS[GUARDIAN_DEF_INDEX]
            guardian_questions = gdef.get('questions', [])
            if guardian_required is None:
                guardian_required = gdef.get('required_score', 0)
            GUARDIAN_DEF_INDEX += 1
        else:
            if not QUESTION_SETS:
                QUESTION_SETS = load_questions_from_json()
            question_index = len(guardians) % max(1, len(QUESTION_SETS))
            guardian_questions = QUESTION_SETS[question_index]
    if guardian_required is None:
        guardian_required = 0
    new_guardian = Guardian(gx, gy, required_score=guardian_required, questions=guardian_questions)
    guardians.append(new_guardian)
    try:
        cx, cy = world_point_to_cell(r['x'] + r.get('w', 0)//2, r['y'] + r.get('h', 0)//2)
        occupied_cells.add((cx, cy))
    except Exception:
        pass


def generate_initial_rooms(num_rooms=3):
    generated_rooms = []
    attempts = 0
    max_attempts = 100
    while len(generated_rooms) < num_rooms and attempts < max_attempts:
        attempts += 1
        min_w, max_w = 180, 280
        min_h, max_h = 120, 200
        w = random.randint(min_w, max_w)
        h = random.randint(min_h, max_h)
        margin = 50
        x = random.randint(margin, WIDTH - w - margin)
        y = random.randint(60 + margin, HEIGHT - h - margin)
        new_room = {'x': x, 'y': y, 'w': w, 'h': h}
        def rooms_overlap(a, b):
            return pygame.Rect(a['x'], a['y'], a['w'], a['h']).colliderect(pygame.Rect(b['x'], b['y'], b['w'], b['h']))
        if not any(rooms_overlap(new_room, existing) for existing in generated_rooms):
            generated_rooms.append(new_room)
            cx, cy = world_point_to_cell(x + w//2, y + h//2)
            occupied_cells.add((cx, cy))
            print(f'[init] generated room {len(generated_rooms)} at ({x},{y},{w},{h}) - grid cell ({cx},{cy})')
        else:
            print(f'[init] room attempt {attempts} rejected due to overlap')
    if len(generated_rooms) < num_rooms:
        print(f'[init] warning: only generated {len(generated_rooms)} rooms out of {num_rooms} requested')
    return generated_rooms


def load_assets():
    global floor, wall, player_img, book_img, font, big_font
    # prefer pgzero `images` if available, else load from IMG_DIR
    p_images = getattr(pgzero, 'images', None)
    def try_img(name, size=None, fallback_color=(255,0,255)):
        key = Path(name).stem
        surf = None
        if p_images is not None:
            try:
                surf = getattr(p_images, key)
            except Exception:
                surf = None
        if surf:
            if size:
                try:
                    return pygame.transform.scale(surf, size)
                except Exception:
                    return surf
            return surf
        return load_image(name, fallback_color=fallback_color, size=size)

    floor = try_img('floor.png', size=(64, 64), fallback_color=(200,200,200))
    wall = try_img('wall.png', size=(64, 64), fallback_color=(120,120,120))
    player_img = try_img('player.png', size=(32, 32), fallback_color=(30,144,255))
    book_img = try_img('book.png', size=(32, 32), fallback_color=(255,215,0))
    # fonts via pygame; ensure fallback fonts exist
    try:
        font = pygame.font.SysFont('arial', 18)
        big_font = pygame.font.SysFont('arial', 24, bold=True)
    except Exception:
        try:
            font = pygame.font.Font(None, 18)
            big_font = pygame.font.Font(None, 24)
        except Exception:
            font = None
            big_font = None


def ensure_fonts():
    """Ensure pygame.font is initialized and fonts are created. Safe to call every frame."""
    global font, big_font
    try:
        if not pygame.font.get_init():
            try:
                pygame.font.init()
            except Exception:
                pass
        if font is None or big_font is None:
            try:
                font = pygame.font.SysFont('arial', 18)
                big_font = pygame.font.SysFont('arial', 24, bold=True)
            except Exception:
                try:
                    font = pygame.font.Font(None, 18)
                    big_font = pygame.font.Font(None, 24)
                except Exception:
                    font = None
                    big_font = None
    except Exception:
        # worst-case, leave fonts as None
        font = None
        big_font = None


def init_game():
    global rooms, books, guardians, px, py, player_score, show_completion
    global QUESTION_SETS, GAME_BOOK_DEFS, GAME_GUARDIAN_DEFS, GAME_PLACEMENTS
    # preload question sets and full game data from game.json
    QUESTION_SETS = load_questions_from_json()
    load_game_data()
    rooms = generate_initial_rooms(3)
    books.clear()
    guardians.clear()
    # place books from placements if specified, ensuring they're inside rooms
    placements_books = GAME_PLACEMENTS.get('books', []) if GAME_PLACEMENTS else []
    for pb in placements_books:
        bid = pb.get('book_id')
        bx = pb.get('x')
        by = pb.get('y')
        if bx is None or by is None:
            continue
        # find a room containing the placement
        placed = False
        for r in rooms:
            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
            if rr.collidepoint(bx, by):
                # place specific book at coords
                bdef = GAME_BOOK_DEFS.get(bid) if bid else None
                if bdef:
                    books.append(Book(bx, by, text=bdef.get('text', 'Livro.'), points=bdef.get('points', 1)))
                else:
                    books.append(Book(bx, by, text='Livro gerado na sala.', points=2))
                PLACED_BOOK_IDS.add(bid) if bid else None
                placed = True
                break
        if not placed:
            # create a small room around the placement and add it
            w, h = 220, 160
            x = max(50, min(int(bx - w//2), WIDTH - w - 50))
            y = max(60, min(int(by - h//2), HEIGHT - h - 60))
            new_room = {'x': x, 'y': y, 'w': w, 'h': h}
            rooms.append(new_room)
            cx, cy = world_point_to_cell(x + w//2, y + h//2)
            occupied_cells.add((cx, cy))
            bdef = GAME_BOOK_DEFS.get(bid) if bid else None
            if bdef:
                books.append(Book(bx, by, text=bdef.get('text', 'Livro.'), points=bdef.get('points', 1)))
            else:
                books.append(Book(bx, by, text='Livro gerado na sala.', points=2))
            PLACED_BOOK_IDS.add(bid) if bid else None

    # place guardians from defs (ensure inside rooms)
    for gdef in GAME_GUARDIAN_DEFS:
        gx = gdef.get('x')
        gy = gdef.get('y')
        questions = gdef.get('questions') or []
        required = gdef.get('required_score', 0)
        if gx is None or gy is None:
            continue
        placed = False
        for r in rooms:
            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
            if rr.collidepoint(gx, gy):
                guardians.append(Guardian(gx, gy, required_score=required, questions=questions))
                placed = True
                break
        if not placed:
            # create a small room around guardian and add it
            w, h = 220, 160
            x = max(50, min(int(gx - w//2), WIDTH - w - 50))
            y = max(60, min(int(gy - h//2), HEIGHT - h - 60))
            new_room = {'x': x, 'y': y, 'w': w, 'h': h}
            rooms.append(new_room)
            cx, cy = world_point_to_cell(x + w//2, y + h//2)
            occupied_cells.add((cx, cy))
            guardians.append(Guardian(gx, gy, required_score=required, questions=questions))

    # ensure every room has a book and guardian; use GAME lists where possible
    for r in rooms:
        rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
        has_book = any(rr.colliderect(pygame.Rect(b.x, b.y, b.w, b.h)) for b in books)
        has_guard = any(rr.colliderect(pygame.Rect(g.x, g.y, g.w, g.h)) for g in guardians)
        if not has_book:
            place_book_in_room(r)
        if not has_guard:
            place_guardian_in_room(r)
    load_assets()


def handle_interact():
    global mode, active_book, read_lines, scroll_y, active_guardian, g_questions, g_choices, g_selected, g_results, g_q_index
    pr = pygame.Rect(int(px) - 24, int(py) - 24, 48, 48)
    # check for book
    for b in books:
        if pr.colliderect(b.rect()) and not b.read:
            mode = 'reading'
            active_book = b
            read_lines = textwrap.wrap(b.text, width=60)
            scroll_y = 0
            global read_page
            read_page = 0
            return
    # check for guardian
    for g in guardians:
        if pr.colliderect(g.rect()) and not g.defeated:
            guardian_book = None
            # First try: find the room containing the guardian and any book inside that room
            guardian_room = None
            for r in rooms:
                rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
                # check guardian center is inside room
                if rr.collidepoint(int(g.x + g.w / 2), int(g.y + g.h / 2)):
                    guardian_room = r
                    break
            if guardian_room is not None:
                room_rect = pygame.Rect(guardian_room['x'], guardian_room['y'], guardian_room['w'], guardian_room['h'])
                for b in books:
                    if room_rect.colliderect(pygame.Rect(b.x, b.y, b.w, b.h)):
                        guardian_book = b
                        break
            # fallback: proximity check (if no book found in the same room)
            if guardian_book is None:
                for b in books:
                    if pygame.Rect(b.x, b.y, b.w, b.h).colliderect(pygame.Rect(g.x - 1, g.y - 1, g.w + 2, g.h + 2)):
                        guardian_book = b
                        break
            if guardian_book is None or not guardian_book.read:
                mode = 'reading'
                active_book = None
                read_lines = ['Você deve ler o livro desta sala antes de falar com o guardião.']
                scroll_y = 0
                read_page = 0
            elif player_score < g.required_score:
                mode = 'reading'
                active_book = None
                read_lines = [f'Você precisa de {g.required_score} pontos para conversar com o guardião.']
                scroll_y = 0
                read_page = 0
            else:
                mode = 'guard_question'
                active_guardian = g
                g_questions = g.questions
                g_choices = [q.get('choices', []) for q in g_questions]
                g_selected = [None] * len(g_questions)
                g_results = [None] * len(g_questions)
                g_q_index = 0
                print(f'[guard] starting questions ({len(g_questions)} items) for guardian at ({g.x},{g.y})')
            return


def update():
    # called by pgzero every frame
    global px, py, player_score, mode, result_timer, show_completion, completion_timer
    dt = DT
    if mode == 'play':
        # Prefer pgzero keyboard if available (returns truthy mapping for keys)
        if PGZ_KEYBOARD is not None and PGZ_KEYS is not None:
            k = PGZ_KEYBOARD
            K = PGZ_KEYS
            dx = (1 if k[K.RIGHT] else 0) - (1 if k[K.LEFT] else 0)
            dy = (1 if k[K.DOWN] else 0) - (1 if k[K.UP] else 0)
        else:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        px += dx * speed * dt
        py += dy * speed * dt

    if mode == 'guard_question_results':
        result_timer += dt
        if result_timer > 3.0:
            reset_guard_question_state()

    if not show_completion:
        remaining = len([g for g in guardians if not g.defeated])
        if remaining == 0:
            show_completion = True
            completion_timer = 0.0
            print('[game] player answered all guardians')

    if show_completion:
        completion_timer += dt


def reset_guard_question_state():
    global mode, g_questions, g_choices, g_selected, g_results, g_q_index, active_guardian, result_timer
    mode = 'play'
    g_questions = []
    g_choices = []
    g_selected = []
    g_results = []
    g_q_index = 0
    active_guardian = None
    result_timer = 0.0


def on_key_down(key):
    global mode, scroll_y, active_book, player_score, g_q_index, g_selected, g_results, result_timer
    # allow pgzero keys constants if available
    K_ESC = PGZ_KEYS.ESCAPE if PGZ_KEYS is not None else pygame.K_ESCAPE
    K_E = PGZ_KEYS.E if PGZ_KEYS is not None else pygame.K_e
    K_UP = PGZ_KEYS.UP if PGZ_KEYS is not None else pygame.K_UP
    K_DOWN = PGZ_KEYS.DOWN if PGZ_KEYS is not None else pygame.K_DOWN
    K_SPACE = PGZ_KEYS.SPACE if PGZ_KEYS is not None else pygame.K_SPACE
    K_1 = PGZ_KEYS.K_1 if PGZ_KEYS is not None else pygame.K_1
    K_2 = PGZ_KEYS.K_2 if PGZ_KEYS is not None else pygame.K_2
    K_3 = PGZ_KEYS.K_3 if PGZ_KEYS is not None else pygame.K_3
    K_KP1 = PGZ_KEYS.K_KP1 if PGZ_KEYS is not None else pygame.K_KP1
    K_KP2 = PGZ_KEYS.K_KP2 if PGZ_KEYS is not None else pygame.K_KP2
    K_KP3 = PGZ_KEYS.K_KP3 if PGZ_KEYS is not None else pygame.K_KP3
    K_RIGHT = PGZ_KEYS.RIGHT if PGZ_KEYS is not None else pygame.K_RIGHT
    K_LEFT = PGZ_KEYS.LEFT if PGZ_KEYS is not None else pygame.K_LEFT

    if key == K_ESC:
        sys.exit(0)
    if mode == 'play':
        if key == K_E:
            handle_interact()
    elif mode == 'reading':
        # page-based reading: LEFT/RIGHT or UP/DOWN to scroll small amounts
        global read_page
        if key == K_UP:
            scroll_y = max(scroll_y - 40, 0)
        elif key == K_DOWN:
            scroll_y += 40
        elif key == K_LEFT:
            read_page = max(0, read_page - 1)
            scroll_y = 0
        elif key == K_RIGHT or key == K_SPACE:
            # advance page or finish
            read_page += 1
            scroll_y = 0
            # if we exhausted pages, mark read and return to play
            # define lines per page heuristically
            lines_per_page = max(1, (300 - 20) // 22)
            total_pages = (len(read_lines) + lines_per_page - 1) // lines_per_page
            if read_page >= total_pages:
                if active_book is not None:
                    active_book.read = True
                    player_score += active_book.points
                    # also mark any other book in the same room as read so guardian can detect it
                    try:
                        # find room containing the active book
                        a_rx = None
                        for r in rooms:
                            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
                            if rr.colliderect(pygame.Rect(active_book.x, active_book.y, active_book.w, active_book.h)):
                                a_rx = rr
                                break
                        if a_rx is not None:
                            for b2 in books:
                                if a_rx.colliderect(pygame.Rect(b2.x, b2.y, b2.w, b2.h)):
                                    b2.read = True
                    except Exception:
                        pass
                mode = 'play'
                active_book = None
                read_page = 0
    elif mode == 'guard_question':
        if key in (K_1, K_KP1):
            g_selected[g_q_index] = 0
        elif key in (K_2, K_KP2):
            g_selected[g_q_index] = 1
        elif key in (K_3, K_KP3):
            g_selected[g_q_index] = 2
        elif key == K_RIGHT:
            g_q_index = min(len(g_questions)-1, g_q_index+1)
        elif key == K_LEFT:
            g_q_index = max(0, g_q_index-1)
        elif key == K_SPACE:
            # confirm answer for current question
            if 0 <= g_q_index < len(g_selected) and g_selected[g_q_index] is not None:
                sel = g_selected[g_q_index]
                q = g_questions[g_q_index]
                try:
                    if sel is None:
                        is_correct = False
                    else:
                        choice_text = str(g_choices[g_q_index][int(sel)])
                        is_correct = (choice_text.strip().lower() == str(q.get('answer')).strip().lower())
                except Exception:
                    is_correct = False
                g_results[g_q_index] = is_correct
                # move to next unanswered question
                next_unanswered = None
                for idx in range(len(g_questions)):
                    if g_results[idx] is None:
                        next_unanswered = idx
                        break
                if next_unanswered is not None:
                    g_q_index = next_unanswered
                else:
                    # finished all questions
                    correct = sum(1 for r in g_results if r)
                    if active_guardian is not None:
                        active_guardian.defeated = True
                    awarded = sum(1 for r in g_results if r)
                    player_score += awarded
                    # spawn new room if any awarded points
                    if awarded > 0 and active_guardian is not None:
                        base_room = None
                        for r in rooms:
                            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
                            if rr.contains(pygame.Rect(active_guardian.x, active_guardian.y, active_guardian.w, active_guardian.h)):
                                base_room = r
                                break
                        if base_room is None and rooms:
                            base_room = random.choice(rooms)
                        if base_room is not None:
                            newr = add_adjacent_room(base_room=base_room)
                            if newr:
                                populate_room_with_book_guard(newr)
                    mode = 'guard_question_results'
                    result_timer = 0.0
    elif mode == 'guard_question_results':
        if key == K_SPACE:
            reset_guard_question_state()


def draw():
    # Render to the pygame display surface. pgzero sets up the display for us.
    global floor, wall, player_img, book_img
    ensure_fonts()
    surf = pygame.display.get_surface()
    if surf is None:
        return
    # pgzero screen helper for text if available
    PGSCR = getattr(pgzero, 'screen', None)
    surf.fill((0, 0, 0))
    cam_x = int(px - WIDTH // 2)
    cam_y = int(py - HEIGHT // 2)
    # background tiles
    for x in range(cam_x - (cam_x % 64) - 64, cam_x + WIDTH + 64, 64):
        for y in range(cam_y - (cam_y % 64) - 64, cam_y + HEIGHT + 64, 64):
            sx = x - cam_x
            sy = y - cam_y
            try:
                surf.blit(floor, (sx, sy))
            except Exception:
                pass
    # rooms
    for r in rooms:
        rx = r['x'] - cam_x
        ry = r['y'] - cam_y
        pygame.draw.rect(surf, (170, 170, 170), (rx, ry, r['w'], r['h']))
        try:
            surf.blit(wall, (rx, ry))
        except Exception:
            pass
    # books
    for b in books:
        bx = b.x - cam_x
        by = b.y - cam_y
        if not b.read:
            try:
                surf.blit(book_img, (bx, by))
            except Exception:
                pygame.draw.rect(surf, (255, 215, 0), (bx, by, b.w, b.h))
        else:
            s = pygame.Surface((b.w, b.h), pygame.SRCALPHA)
            s.fill((100, 100, 100, 180))
            surf.blit(s, (bx, by))
    # guardians
    for g in guardians:
        gx = g.x - cam_x
        gy = g.y - cam_y
        color = (200, 50, 50) if not g.defeated else (80, 160, 80)
        pygame.draw.rect(surf, color, (gx, gy, g.w, g.h))
    # player
    try:
        surf.blit(player_img, (int(px - cam_x) - 16, int(py - cam_y) - 16))
    except Exception:
        pygame.draw.circle(surf, (30,144,255), (int(px - cam_x), int(py - cam_y)), 10)
    # HUD
    unread_book_points = sum(b.points for b in books if not b.read)
    remaining_questions = sum(len(g.questions) for g in guardians if not g.defeated)
    max_possible = player_score + unread_book_points + remaining_questions
    hud_text = f'Score: {player_score}  |  Max possible: {max_possible}'
    if PGSCR is not None and hasattr(PGSCR, 'draw'):
        # choose a fontsize similar to the fonts
        PGSCR.draw.text(hud_text, (10, 10), color='white', fontsize=24 if big_font else 18)
    else:
        if big_font:
            hud_surf = big_font.render(hud_text, True, (255,255,255))
            surf.blit(hud_surf, (10, 10))
        else:
            if font:
                hud_surf = font.render(hud_text, True, (255,255,255))
                surf.blit(hud_surf, (10,10))
    # interaction hint
    pr = pygame.Rect(int(px) - 24, int(py) - 24, 48, 48)
    near_text = ''
    for b in books:
        if pr.colliderect(b.rect()) and not b.read:
            near_text = 'Press E to read book'
    for g in guardians:
        if pr.colliderect(g.rect()) and not g.defeated:
            near_text = f"Press E to talk (requires {g.required_score} pts)"
    if near_text:
        if PGSCR is not None and hasattr(PGSCR, 'draw'):
            PGSCR.draw.text(near_text, (10, HEIGHT - 30), color='yellow', fontsize=18)
        else:
            if font:
                tip = font.render(near_text, True, (255,255,0))
                surf.blit(tip, (10, HEIGHT - 30))
    # minimap (simple)
    try:
        mm_w, mm_h = 180, 140
        mm_x, mm_y = WIDTH - mm_w - 10, 10
        mm_surf = pygame.Surface((mm_w, mm_h), pygame.SRCALPHA)
        mm_surf.fill((40,40,60,128))
        surf.blit(mm_surf, (mm_x, mm_y))
        if rooms:
            min_x = min(r['x'] for r in rooms)
            min_y = min(r['y'] for r in rooms)
            max_x = max(r['x'] + r['w'] for r in rooms)
            max_y = max(r['y'] + r['h'] for r in rooms)
        else:
            min_x = 0; min_y = 0; max_x = WIDTH; max_y = HEIGHT
        world_w = max(1, max_x - min_x)
        world_h = max(1, max_y - min_y)
        scale = min(mm_w / world_w, mm_h / world_h)
        for r in rooms:
            rx = int((r['x'] - min_x) * scale)
            ry = int((r['y'] - min_y) * scale)
            rw = max(2, int(r['w'] * scale))
            rh = max(2, int(r['h'] * scale))
            pygame.draw.rect(surf, (100,100,140), (mm_x + rx, mm_y + ry, rw, rh))
        for g in guardians:
            color = (200,50,50) if not g.defeated else (80,160,80)
            gx = int((g.x - min_x) * scale)
            gy = int((g.y - min_y) * scale)
            pygame.draw.circle(surf, color, (mm_x + gx, mm_y + gy), 3)
        px_mm = int((px - min_x) * scale)
        py_mm = int((py - min_y) * scale)
        pygame.draw.circle(surf, (30,144,255), (mm_x + px_mm, mm_y + py_mm), 4)
    except Exception:
        pass
    # reading UI
    if mode == 'reading' and read_lines:
        box_h = 300
        box_w = 700
        box_x = 50
        box_y = 120
        # semi-transparent backdrop
        back = pygame.Surface((box_w + 8, box_h + 8), pygame.SRCALPHA)
        back.fill((20, 20, 40, 200))
        surf.blit(back, (box_x - 4, box_y - 4))
        pygame.draw.rect(surf, (240, 240, 240), (box_x, box_y, box_w, box_h))
        # compute scrolling limits
        line_h = 22
        content_h = len(read_lines) * line_h
        max_scroll = max(0, content_h - (box_h - 20))
        # clamp scroll_y so drawing can't overflow
        global scroll_y
        scroll_y = max(0, min(scroll_y, max_scroll))
        y = box_y + 10 - scroll_y
        for line in read_lines:
            if PGSCR is not None and hasattr(PGSCR, 'draw'):
                # pgzero draw.text expects top-left, choose fontsize
                PGSCR.draw.text(line, (box_x + 10, y), color=(10,10,10), fontsize=18)
            else:
                if font:
                    img = font.render(line, True, (10, 10, 10))
                    surf.blit(img, (box_x + 10, y))
            y += line_h
        hint = 'Use UP/DOWN to scroll, SPACE to finish'
        if font:
            hint_img = font.render(hint, True, (80, 80, 80))
            surf.blit(hint_img, (box_x + 10, box_y + box_h - 30))
    # guardian question UI
    if (mode == 'guard_question' or mode == 'guard_question_results') and g_questions:
        box_h = 320
        box_w = 720
        box_x = 40
        box_y = 80
        # backdrop with alpha
        back = pygame.Surface((box_w + 8, box_h + 8), pygame.SRCALPHA)
        back.fill((30, 30, 60, 220))
        surf.blit(back, (box_x - 4, box_y - 4))
        pygame.draw.rect(surf, (250, 250, 250), (box_x, box_y, box_w, box_h))
        # guard against invalid index
        if g_q_index < 0 or g_q_index >= len(g_questions):
            return
        q = g_questions[g_q_index]
        # wrap question text to multiple lines
        qtext = f"Q{g_q_index+1}: {q.get('question','') }"
        wrap_width = 80 if big_font else 60
        q_lines = textwrap.wrap(qtext, width=wrap_width)
        line_h = 22
        yoff = box_y + 10
        for ln in q_lines:
            if PGSCR is not None and hasattr(PGSCR, 'draw'):
                PGSCR.draw.text(ln, (box_x + 10, yoff), color=(10,10,10), fontsize=24 if big_font else 18)
            else:
                if big_font:
                    qtxt = big_font.render(ln, True, (10, 10, 10))
                    surf.blit(qtxt, (box_x + 10, yoff))
                else:
                    if font:
                        qtxt = font.render(ln, True, (10, 10, 10))
                        surf.blit(qtxt, (box_x + 10, yoff))
            yoff += line_h
        # choices
        choices = g_choices[g_q_index]
        base_y = box_y + 20 + len(q_lines) * line_h
        for i, choice in enumerate(choices):
            prefix = str(i+1) + ') '
            sel = (g_selected and g_selected[g_q_index] == i)
            col = (40, 40, 40)
            choice_y = base_y + i * 30
            # selection highlight
            if mode == 'guard_question' and sel:
                bg = pygame.Surface((box_w - 40, 28), pygame.SRCALPHA)
                bg.fill((180, 210, 255, 255))
                surf.blit(bg, (box_x + 20, choice_y - 2))
                col = (10, 40, 140)
            answered = (g_results and g_results[g_q_index] is not None)
            if answered or (mode == 'guard_question_results' and g_results):
                correct_index = None
                ans = q.get('answer')
                for ci, ch in enumerate(choices):
                    if str(ch).strip().lower() == str(ans).strip().lower():
                        correct_index = ci
                        break
                if correct_index is not None and i == correct_index:
                    bg = pygame.Surface((box_w - 40, 28), pygame.SRCALPHA)
                    bg.fill((200, 255, 200, 255))
                    surf.blit(bg, (box_x + 20, choice_y - 2))
                    col = (0, 120, 0)
                elif g_selected[g_q_index] == i and (g_results and not g_results[g_q_index]):
                    bg = pygame.Surface((box_w - 40, 28), pygame.SRCALPHA)
                    bg.fill((255, 200, 200, 255))
                    surf.blit(bg, (box_x + 20, choice_y - 2))
                    col = (160, 0, 0)
                else:
                    col = (100, 100, 100)
            # draw choice text
            choice_text = prefix + str(choice)
            if PGSCR is not None and hasattr(PGSCR, 'draw'):
                PGSCR.draw.text(choice_text, (box_x + 20, choice_y), color=col, fontsize=18)
            else:
                if font:
                    txt = font.render(choice_text, True, col)
                    surf.blit(txt, (box_x + 20, choice_y))
        # footer: controls description
        controls = 'Controles: 1/2/3 = selecionar, ←/→ = navegar perguntas, Espaço = confirmar'
        ctrl_y = box_y + box_h - 28
        if PGSCR is not None and hasattr(PGSCR, 'draw'):
            PGSCR.draw.text(controls, (box_x + 10, ctrl_y), color=(80, 80, 80), fontsize=16)
        else:
            if font:
                ctrl_img = font.render(controls, True, (80, 80, 80))
                surf.blit(ctrl_img, (box_x + 10, ctrl_y))


# Call init on import so pgzero can start immediately
init_game()


# expose helper used in update when creating new rooms
def add_adjacent_room(base_room=None, max_tries=50):
    # duplicate smaller version of original add_adjacent_room used by game logic
    def rooms_overlap(room1, room2):
        r1 = pygame.Rect(room1['x'], room1['y'], room1['w'], room1['h'])
        r2 = pygame.Rect(room2['x'], room2['y'], room2['w'], room2['h'])
        return r1.colliderect(r2)
    base = base_room or (random.choice(rooms) if rooms else None)
    if base is None:
        return None
    for attempt in range(max_tries):
        w = random.randint(180, 280)
        h = random.randint(120, 200)
        margin = 60
        directions = [
            (base['x'] + base['w'] + margin, base['y']),
            (base['x'] - w - margin, base['y']),
            (base['x'], base['y'] + base['h'] + margin),
            (base['x'], base['y'] - h - margin),
        ]
        random.shuffle(directions)
        for x, y in directions:
            if x < 50 or y < 60 or x + w > MAP_WIDTH - 50 or y + h > MAP_HEIGHT - 50:
                continue
            new_room = {'x': x, 'y': y, 'w': w, 'h': h}
            if not any(rooms_overlap(new_room, existing) for existing in rooms):
                rooms.append(new_room)
                cx, cy = world_point_to_cell(x + w//2, y + h//2)
                occupied_cells.add((cx, cy))
                print(f'[spawn] added room at ({x},{y},{w},{h}) adjacent to base ({base["x"]},{base["y"]})')
                return new_room
    for attempt in range(max_tries):
        w = random.randint(180, 280)
        h = random.randint(120, 200)
        x = random.randint(50, MAP_WIDTH - w - 50)
        y = random.randint(60, MAP_HEIGHT - h - 50)
        new_room = {'x': x, 'y': y, 'w': w, 'h': h}
        if not any(rooms_overlap(new_room, existing) for existing in rooms):
            rooms.append(new_room)
            cx, cy = world_point_to_cell(x + w//2, y + h//2)
            occupied_cells.add((cx, cy))
            print(f'[spawn] added room at ({x},{y},{w},{h}) via random placement')
            return new_room
    print('[spawn] failed to add room - no free space found anywhere')
    return None


if __name__ == '__main__':
    try:
        import pgzrun
        pgzrun.go()
    except Exception:
        # fallback: run pygame main loop if pgzero isn't available
        print('pgzero/pgzrun not available - run this module with pgzero (pgzrun)')
