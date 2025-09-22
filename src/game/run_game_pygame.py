"""Standalone pygame runner to force a visible window and draw the map + player.

Use arrow keys to move. Loads images from src/game/images if available.
"""
import pygame
import random
from pathlib import Path
import sys
import textwrap
import json
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / 'src' / 'game' / 'images'

WIDTH, HEIGHT = 800, 600
FPS = 60


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
        json_path = ROOT / 'src' / 'game' / 'game.json'
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Run Game (pygame standalone) - Books & Guardians')
    clock = pygame.time.Clock()

    # occupancy grid settings (discrete cells for rooms to guarantee empty-adjacent placement)
    GRID_CELL_W = 320
    GRID_CELL_H = 240
    GRID_MARGIN_X = 40
    GRID_MARGIN_Y = 60
    # set of occupied cells as (cx, cy)
    occupied_cells = set()


    # helper: add rooms adjacent to existing rooms (up/down/left/right)
    def world_point_to_cell(x, y):
        # match the cell_coords_from_point logic used elsewhere: floor division
        cx = int((x - GRID_MARGIN_X) // GRID_CELL_W)
        cy = int((y - GRID_MARGIN_Y) // GRID_CELL_H)
        return cx, cy


    def add_adjacent_room(base_room=None, max_tries=50):
        # helper function to check room overlap
        def rooms_overlap(room1, room2):
            r1 = pygame.Rect(room1['x'], room1['y'], room1['w'], room1['h'])
            r2 = pygame.Rect(room2['x'], room2['y'], room2['w'], room2['h'])
            return r1.colliderect(r2)
        
        def room_overlaps_any_existing(new_room):
            for existing_room in rooms:
                if rooms_overlap(new_room, existing_room):
                    return True
            return False
        
        # determine base room
        base = None
        if base_room:
            base = base_room
        else:
            base = random.choice(rooms) if rooms else None
        
        if base is None:
            return None
        
        # try to create room near base room
        for attempt in range(max_tries):
            # generate room size
            min_w, max_w = 180, 280
            min_h, max_h = 120, 200
            w = random.randint(min_w, max_w)
            h = random.randint(min_h, max_h)
            
            # try different positions around base room
            margin = 60  # minimum distance from base room
            directions = [
                (base['x'] + base['w'] + margin, base['y']),  # right
                (base['x'] - w - margin, base['y']),           # left
                (base['x'], base['y'] + base['h'] + margin),   # below
                (base['x'], base['y'] - h - margin),           # above
                # diagonal positions
                (base['x'] + base['w'] + margin, base['y'] + base['h'] + margin),  # bottom-right
                (base['x'] - w - margin, base['y'] - h - margin),                   # top-left
                (base['x'] + base['w'] + margin, base['y'] - h - margin),           # top-right
                (base['x'] - w - margin, base['y'] + base['h'] + margin),           # bottom-left
            ]
            
            random.shuffle(directions)
            
            for x, y in directions:
                # check bounds
                if x < 50 or y < 60 or x + w > WIDTH - 50 or y + h > HEIGHT - 50:
                    continue
                
                new_room = {'x': x, 'y': y, 'w': w, 'h': h}
                
                # check if room overlaps with any existing room
                if not room_overlaps_any_existing(new_room):
                    rooms.append(new_room)
                    # mark grid cell as occupied
                    cx, cy = world_point_to_cell(x + w//2, y + h//2)
                    occupied_cells.add((cx, cy))
                    print(f'[spawn] added room at ({x},{y},{w},{h}) adjacent to base ({base["x"]},{base["y"]})')
                    return new_room
        
        # if adjacent placement failed, try random placement anywhere on map
        print('[spawn] adjacent placement failed, trying random placement...')
        for attempt in range(max_tries):
            # generate room size
            w = random.randint(180, 280)
            h = random.randint(120, 200)
            
            # try random position on map
            x = random.randint(50, WIDTH - w - 50)
            y = random.randint(60, HEIGHT - h - 50)
            
            new_room = {'x': x, 'y': y, 'w': w, 'h': h}
            
            # check if room overlaps with any existing room
            if not room_overlaps_any_existing(new_room):
                rooms.append(new_room)
                # mark grid cell as occupied
                cx, cy = world_point_to_cell(x + w//2, y + h//2)
                occupied_cells.add((cx, cy))
                print(f'[spawn] added room at ({x},{y},{w},{h}) via random placement')
                return new_room
        
        print('[spawn] failed to add room - no free space found anywhere')
        return None

    def add_rooms(n):
        for _ in range(n):
            base = random.choice(rooms) if rooms else None
            newr = add_adjacent_room(base_room=base)
            # for each new room, populate atomically with exactly one book and one guardian
            if newr is not None:
                populate_room_with_book_guard(newr)
                print(f'[spawn] created room + populated with book+guardian at ({newr["x"]},{newr["y"]})')

    def spawn_guardians(n, pick_rooms=None):
        # spawn n guardians, selecting rooms from pick_rooms or random existing rooms
        for i in range(n):
            # pick candidate rooms
            candidate_rooms = list(pick_rooms) if pick_rooms else list(rooms)

            def room_has_guardian(room):
                rr = pygame.Rect(room['x'], room['y'], room['w'], room['h'])
                for g in guardians:
                    if rr.colliderect(g.rect()):
                        return True
                return False

            # rooms without guardians
            free_rooms = [r for r in candidate_rooms if not room_has_guardian(r)]

            # if none available, try creating a new adjacent room and populate it
            if not free_rooms:
                base = random.choice(rooms) if rooms else None
                newr = add_adjacent_room(base_room=base)
                if newr:
                    populate_room_with_book_guard(newr)
                    free_rooms = [newr]

            # if still none, fallback to a central room-like dict
            if free_rooms:
                r = random.choice(free_rooms)
            else:
                r = {'x': WIDTH//2 - 100, 'y': HEIGHT//2 - 50, 'w': 200, 'h': 120}

            # place guardian roughly in room center (if r is a dict from populate, use its geometry)
            gx = r['x'] + r['w']//2 + random.randint(-20, 20)
            gy = r['y'] + r['h']//2 + random.randint(-20, 20)
            # ensure we don't create duplicate guardians in the same room
            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
            already_has_guard = any(rr.colliderect(g.rect()) for g in guardians)
            if not already_has_guard:
                q = make_sample_questions()
                req = max(0, player_score)
                newg = Guardian(gx, gy, required_score=req, questions=q)
                guardians.append(newg)
                print(f'[spawn] guardian at ({gx},{gy}) in room ({r["x"]},{r["y"]})')

    def populate_room_with_book_guard(r):
        # always add exactly one book and one guardian to the room without overlapping
        margin = 15
        book_w, book_h = 32, 32
        guard_w, guard_h = 40, 40
        
        # initialize positions with fallback values
        bx = r['x'] + 5
        by = r['y'] + 5
        gx = r['x'] + 5
        gy = r['y'] + 5
        
        # ensure room is large enough for both entities
        min_width = 2*margin + max(book_w, guard_w) + 50  # extra space between entities
        min_height = 2*margin + max(book_h, guard_h)
        
        if r['w'] >= min_width and r['h'] >= min_height:
            # place book first
            bx = r['x'] + margin + random.randint(0, r['w'] - 2*margin - book_w)
            by = r['y'] + margin + random.randint(0, r['h'] - 2*margin - book_h)
            
            # place guardian ensuring no overlap with book
            attempts = 0
            max_attempts = 20
            while attempts < max_attempts:
                gx = r['x'] + margin + random.randint(0, r['w'] - 2*margin - guard_w)
                gy = r['y'] + margin + random.randint(0, r['h'] - 2*margin - guard_h)
                
                # check if guardian overlaps with book (add some padding)
                book_rect = pygame.Rect(bx - 5, by - 5, book_w + 10, book_h + 10)
                guard_rect = pygame.Rect(gx, gy, guard_w, guard_h)
                
                if not book_rect.colliderect(guard_rect):
                    break  # no overlap, position is good
                
                attempts += 1
            
            # if we couldn't find a non-overlapping position, use fallback
            if attempts >= max_attempts:
                # place them at opposite corners with safe distance
                bx = r['x'] + margin
                by = r['y'] + margin
                gx = r['x'] + r['w'] - margin - guard_w
                gy = r['y'] + r['h'] - margin - guard_h
        else:
            # fallback for very small rooms - place at opposite corners
            bx = r['x'] + 5
            by = r['y'] + 5
            gx = r['x'] + r['w'] - guard_w - 5
            gy = r['y'] + r['h'] - guard_h - 5
            # ensure guardian doesn't go outside room bounds
            gx = max(r['x'] + 5, min(gx, r['x'] + r['w'] - guard_w - 5))
            gy = max(r['y'] + 5, min(gy, r['y'] + r['h'] - guard_h - 5))
        
        books.append(Book(bx, by, text='Livro gerado na sala.', points=2))
        
        # get questions for this guardian - cycle through available question sets
        global QUESTION_SETS
        if not QUESTION_SETS:
            QUESTION_SETS = load_questions_from_json()
        
        # use modulo to cycle through available question sets
        question_index = len(guardians) % len(QUESTION_SETS)
        guardian_questions = QUESTION_SETS[question_index]
        
        # use a neutral required_score when populating rooms at startup; spawn_guardians uses current score
        new_guardian = Guardian(gx, gy, required_score=0, questions=guardian_questions)
        guardians.append(new_guardian)
        print(f'[spawn] added book at ({bx},{by}) and guardian at ({gx},{gy}) in room ({r["x"]},{r["y"]},{r["w"]},{r["h"]})')
        
        # mark occupancy for this room (use center point -> cell)
        try:
            cx, cy = world_point_to_cell(r['x'] + r.get('w', 0)//2, r['y'] + r.get('h', 0)//2)
            occupied_cells.add((cx, cy))
        except Exception:
            pass

    floor = load_image('floor.png', fallback_color=(200, 200, 200), size=(64, 64))
    wall = load_image('wall.png', fallback_color=(120, 120, 120), size=(64, 64))
    player_img = load_image('player.png', fallback_color=(30, 144, 255), size=(32, 32))
    book_img = load_image('book.png', fallback_color=(255, 215, 0), size=(32, 32))

    # start with 3 rooms; each will be populated with one book and one guardian below
    rooms = []
    
    # generate rooms in free areas using grid system
    def generate_initial_rooms(num_rooms=3):
        generated_rooms = []
        attempts = 0
        max_attempts = 100
        
        def rooms_overlap(room1, room2):
            # check if two rooms overlap
            r1 = pygame.Rect(room1['x'], room1['y'], room1['w'], room1['h'])
            r2 = pygame.Rect(room2['x'], room2['y'], room2['w'], room2['h'])
            return r1.colliderect(r2)
        
        def room_overlaps_any_existing(new_room, existing_rooms):
            # check if new room overlaps with any existing room
            for existing_room in existing_rooms:
                if rooms_overlap(new_room, existing_room):
                    return True
            return False
        
        while len(generated_rooms) < num_rooms and attempts < max_attempts:
            attempts += 1
            
            # generate random room size
            min_w, max_w = 180, 280
            min_h, max_h = 120, 200
            w = random.randint(min_w, max_w)
            h = random.randint(min_h, max_h)
            
            # generate random position with margins
            margin = 50  # minimum distance between rooms
            x = random.randint(margin, WIDTH - w - margin)
            y = random.randint(60 + margin, HEIGHT - h - margin)  # 60 for UI space at top
            
            new_room = {'x': x, 'y': y, 'w': w, 'h': h}
            
            # check if this room overlaps with any existing room
            if not room_overlaps_any_existing(new_room, generated_rooms):
                generated_rooms.append(new_room)
                
                # calculate and mark grid cell as occupied
                cx, cy = world_point_to_cell(x + w//2, y + h//2)
                occupied_cells.add((cx, cy))
                
                print(f'[init] generated room {len(generated_rooms)} at ({x},{y},{w},{h}) - grid cell ({cx},{cy})')
            else:
                print(f'[init] room attempt {attempts} rejected due to overlap')
        
        if len(generated_rooms) < num_rooms:
            print(f'[init] warning: only generated {len(generated_rooms)} rooms out of {num_rooms} requested')
        
        return generated_rooms
    
    rooms = generate_initial_rooms(3)

    # initialize empty lists - will be populated by room generation
    books = []
    guardians = []
    
    # check if game.json exists for custom configuration, but don't populate entities from it
    GAME_JSON = ROOT / 'src' / 'game' / 'game.json'
    if GAME_JSON.exists():
        print('[init] game.json found but using procedural generation instead')

    # populate initial rooms: ensure each starting room has 1 book and 1 guardian
    for r in rooms:
        populate_room_with_book_guard(r)
        print(f'[init] populated room at ({r["x"]},{r["y"]}) with book and guardian')

    # mark these initial rooms as occupied in the grid (already done in generate_initial_rooms)
    # no additional marking needed

    def get_room_for_guardian(g):
        # return the room dict that contains the guardian (by checking if guardian rect is inside room)
        g_rect = g.rect()
        for r in rooms:
            rr = pygame.Rect(r['x'], r['y'], r['w'], r['h'])
            if rr.contains(g_rect):
                return r
        return None

    def get_book_for_guardian(g):
        # return the book that is in the same room as the guardian
        guardian_room = get_room_for_guardian(g)
        if guardian_room is None:
            return None
        
        # find book in the same room
        room_rect = pygame.Rect(guardian_room['x'], guardian_room['y'], guardian_room['w'], guardian_room['h'])
        for b in books:
            b_rect = b.rect()
            if room_rect.contains(b_rect):
                return b
        return None

    px, py = WIDTH // 2, HEIGHT // 2
    speed = 240

    player_score = 0
    show_completion = False
    completion_timer = 0.0

    # UI states
    mode = 'play'  # 'play', 'reading', 'guard_question'
    active_book = None
    active_guardian = None
    # reading state
    read_lines = []
    scroll_y = 0
    font = pygame.font.SysFont('arial', 18)
    big_font = pygame.font.SysFont('arial', 24, bold=True)

    # guardian question state
    g_questions = []
    g_choices = []
    g_selected: list[Any] = []
    g_q_index = 0
    g_results: list[Any] = []  # None until evaluated, then True/False per question

    running = True
    result_timer = 0.0
    while running:
        dt = clock.tick(FPS) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                if mode == 'play':
                    if ev.key == pygame.K_e:
                        # check for nearby book
                        interacted = False
                        pr = pygame.Rect(px - 24, py - 24, 48, 48)
                        for b in books:
                            if pr.colliderect(b.rect()) and not b.read:
                                # start reading
                                mode = 'reading'
                                active_book = b
                                # prepare wrapped lines
                                read_lines = textwrap.wrap(b.text, width=60)
                                scroll_y = 0
                                interacted = True
                                break
                        if interacted:
                            continue
                        # check for guardian
                        for g in guardians:
                            if pr.colliderect(g.rect()) and not g.defeated:
                                # first check if the book in the same room has been read
                                guardian_book = get_book_for_guardian(g)
                                if guardian_book is None or not guardian_book.read:
                                    # show message requiring book to be read first
                                    mode = 'reading'
                                    active_book = None
                                    read_lines = ['Você deve ler o livro desta sala antes de falar com o guardião.']
                                    scroll_y = 0
                                elif player_score < g.required_score:
                                    # show temporary message by starting a short reading-like message
                                    mode = 'reading'
                                    active_book = None
                                    read_lines = [f'Você precisa de {g.required_score} pontos para conversar com o guardião.']
                                    scroll_y = 0
                                else:
                                    # start questions directly - guardian is already properly positioned
                                    mode = 'guard_question'
                                    active_guardian = g
                                    g_questions = g.questions
                                    g_choices = [q.get('choices', []) for q in g_questions]
                                    g_selected = [None] * len(g_questions)
                                    # per-question results: None=not answered, True/False after evaluation
                                    g_results = [None] * len(g_questions)
                                    g_q_index = 0
                                    print(f'[guard] starting questions ({len(g_questions)} items) for guardian at ({g.x},{g.y})')
                                interacted = True
                                break
                    # movement keys handled below
                elif mode == 'reading':
                    # scroll with up/down and finish with space
                    if ev.key == pygame.K_UP:
                        scroll_y = max(scroll_y - 40, 0)
                    elif ev.key == pygame.K_DOWN:
                        scroll_y += 40
                    elif ev.key == pygame.K_SPACE:
                        # if end reached grant points and mark read
                        if active_book is not None:
                            # heuristics: if scrolled to bottom or small text
                            if scroll_y >= max(0, len(read_lines) * 22 - 300):
                                active_book.read = True
                                player_score += active_book.points
                        # exit reading
                        mode = 'play'
                        active_book = None
                        read_lines = []
                        scroll_y = 0
                elif mode == 'guard_question':
                    # map 1/2/3 keys to choices for current question
                    if ev.key == pygame.K_1 or ev.key == pygame.K_KP1:
                        if g_q_index >= len(g_selected):
                            g_selected = (g_selected + [None] * (g_q_index - len(g_selected) + 1))
                        g_selected[g_q_index] = 0
                        print(f'[guard] selected q{g_q_index} -> 0')
                    elif ev.key == pygame.K_2 or ev.key == pygame.K_KP2:
                        if g_q_index >= len(g_selected):
                            g_selected = (g_selected + [None] * (g_q_index - len(g_selected) + 1))
                        g_selected[g_q_index] = 1
                        print(f'[guard] selected q{g_q_index} -> 1')
                    elif ev.key == pygame.K_3 or ev.key == pygame.K_KP3:
                        if g_q_index >= len(g_selected):
                            g_selected = (g_selected + [None] * (g_q_index - len(g_selected) + 1))
                        g_selected[g_q_index] = 2
                        print(f'[guard] selected q{g_q_index} -> 2')
                    elif ev.key == pygame.K_RIGHT:
                        g_q_index = min(len(g_questions)-1, g_q_index+1)
                    elif ev.key == pygame.K_LEFT:
                        g_q_index = max(0, g_q_index-1)
                    elif ev.key == pygame.K_SPACE:
                        # if current question has a selection, evaluate it now (per-question answer)
                        if g_q_index < len(g_selected) and g_selected[g_q_index] is not None:
                            sel = g_selected[g_q_index]
                            q = g_questions[g_q_index]
                            try:
                                is_correct = (g_choices[g_q_index][sel].strip().lower() == str(q.get('answer')).strip().lower())
                            except Exception:
                                is_correct = False
                            # ensure g_results length
                            if g_q_index >= len(g_results):
                                g_results = (g_results + [None] * (g_q_index - len(g_results) + 1))
                            g_results[g_q_index] = is_correct
                            # auto-advance to next unanswered question if any
                            next_unanswered = None
                            for idx in range(len(g_questions)):
                                if g_results[idx] is None:
                                    next_unanswered = idx
                                    break
                            if next_unanswered is not None:
                                g_q_index = next_unanswered
                            else:
                                # all questions have been answered -> show final results
                                correct = sum(1 for r in g_results if r)
                                print(f'[guard] final results: {g_results} -> {correct}/{len(g_questions)} correct')
                                
                                # ALWAYS mark guardian as defeated when all questions answered
                                if active_guardian is not None:
                                    active_guardian.defeated = True
                                    print(f'[guard] guardian at ({active_guardian.x},{active_guardian.y}) defeated')
                                
                                # award points for any True entries in g_results
                                awarded = 0
                                for idx, res in enumerate(g_results):
                                    if res:
                                        awarded += 1
                                player_score += awarded
                                print(f'[score] awarded {awarded} points for correct answers')
                                
                                # ALWAYS generate new room when points are awarded (guardian completed)
                                if awarded > 0 and active_guardian is not None:
                                    # when a guardian is fully answered and points awarded, generate 1 adjacent populated room
                                    base_room = get_room_for_guardian(active_guardian)
                                    if base_room is None and rooms:
                                        base_room = random.choice(rooms)
                                        print(f'[spawn] guardian was not in any room, using random base room')
                                    if base_room is not None:
                                        print(f'[spawn] attempting to create new room adjacent to ({base_room["x"]},{base_room["y"]})')
                                        newr = add_adjacent_room(base_room=base_room)
                                        if newr:
                                            populate_room_with_book_guard(newr)
                                            print(f'[spawn] successfully created and populated new room at ({newr["x"]},{newr["y"]})')
                                        else:
                                            print(f'[spawn] failed to create new room - no free space found')
                                    else:
                                        print(f'[spawn] no base room available for new room generation')
                                
                                mode = 'guard_question_results'
                                result_timer = 0.0
                                # keep active_guardian until results closed
                        else:
                            # if space pressed with no selection, and we're in results mode, allow closing
                            pass
                elif mode == 'guard_question_results':
                    # allow pressing SPACE to close results and return to play
                    if ev.key == pygame.K_SPACE:
                        mode = 'play'
                        g_questions = []
                        g_choices = []
                        g_selected = []
                        g_results = []
                        g_q_index = 0
                        active_guardian = None
                # allow quitting the questionnaire early with Q
                if mode == 'guard_question' and ev.key == pygame.K_q:
                    print('[guard] questionnaire aborted by player')
                    mode = 'play'
                    g_questions = []
                    g_choices = []
                    g_selected = []
                    g_results = []
                    g_q_index = 0
                    active_guardian = None

        # movement
        if mode == 'play':
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
            px += dx * speed * dt
            py += dy * speed * dt

        # camera centered on player
        cam_x = int(px - WIDTH // 2)
        cam_y = int(py - HEIGHT // 2)

        # draw background tiles (world-relative, using camera)
        start_x = cam_x - (cam_x % 64) - 64
        start_y = cam_y - (cam_y % 64) - 64
        for x in range(start_x, cam_x + WIDTH + 64, 64):
            for y in range(start_y, cam_y + HEIGHT + 64, 64):
                sx = x - cam_x
                sy = y - cam_y
                screen.blit(floor, (sx, sy))

        # draw rooms (world -> screen)
        for r in rooms:
            rx = r['x'] - cam_x
            ry = r['y'] - cam_y
            pygame.draw.rect(screen, (170, 170, 170), (rx, ry, r['w'], r['h']))
            # draw wall texture at room top-left
            screen.blit(wall, (rx, ry))

        # draw books (world -> screen)
        for b in books:
            bx = b.x - cam_x
            by = b.y - cam_y
            if not b.read:
                screen.blit(book_img, (bx, by))
            else:
                # dim read books
                s = pygame.Surface((b.w, b.h), pygame.SRCALPHA)
                s.fill((100, 100, 100, 180))
                screen.blit(s, (bx, by))

        # draw guardians (world -> screen)
        for g in guardians:
            gx = g.x - cam_x
            gy = g.y - cam_y
            color = (200, 50, 50) if not g.defeated else (80, 160, 80)
            pygame.draw.rect(screen, color, (gx, gy, g.w, g.h))

        # draw player (world -> screen)
        screen.blit(player_img, (int(px - cam_x) - 16, int(py - cam_y) - 16))

        # HUD: Score and max possible
        # compute max possible remaining points: unread books + total remaining unanswered questions
        unread_book_points = sum(b.points for b in books if not b.read)
        remaining_questions = 0
        for g in guardians:
            if not g.defeated:
                remaining_questions += len(g.questions)
        # each question gives 1 point when correct
        max_possible = player_score + unread_book_points + remaining_questions
        hud = big_font.render(f'Score: {player_score}  |  Max possible: {max_possible}', True, (255, 255, 255))
        screen.blit(hud, (10, 10))

        # interaction hint
        pr = pygame.Rect(px - 24, py - 24, 48, 48)
        near_text = ''
        for b in books:
            if pr.colliderect(b.rect()) and not b.read:
                near_text = 'Press E to read book'
        for g in guardians:
            if pr.colliderect(g.rect()) and not g.defeated:
                near_text = f"Press E to talk (requires {g.required_score} pts)"
        if near_text:
            tip = font.render(near_text, True, (255, 255, 0))
            screen.blit(tip, (10, HEIGHT - 30))

        # minimap (top-right)
        try:
            mm_w, mm_h = 180, 140
            mm_x, mm_y = WIDTH - mm_w - 10, 10
            # minimap background 50% transparent
            mm_surf = pygame.Surface((mm_w, mm_h), pygame.SRCALPHA)
            mm_surf.fill((40, 40, 60, 128))
            screen.blit(mm_surf, (mm_x, mm_y))
            # world bounds from rooms
            if rooms:
                min_x = min(r['x'] for r in rooms)
                min_y = min(r['y'] for r in rooms)
                max_x = max(r['x'] + r['w'] for r in rooms)
                max_y = max(r['y'] + r['h'] for r in rooms)
            else:
                min_x = 0; min_y = 0; max_x = WIDTH; max_y = HEIGHT
            world_w = max(1, max_x - min_x)
            world_h = max(1, max_y - min_y)
            sx = mm_w / world_w
            sy = mm_h / world_h
            scale = min(sx, sy)
            # draw rooms
            for r in rooms:
                rx = int((r['x'] - min_x) * scale)
                ry = int((r['y'] - min_y) * scale)
                rw = max(2, int(r['w'] * scale))
                rh = max(2, int(r['h'] * scale))
                pygame.draw.rect(screen, (100, 100, 140), (mm_x + rx, mm_y + ry, rw, rh))
            # draw guardians
            for g in guardians:
                color = (200, 50, 50) if not g.defeated else (80, 160, 80)
                gx = int((g.x - min_x) * scale)
                gy = int((g.y - min_y) * scale)
                pygame.draw.circle(screen, color, (mm_x + gx, mm_y + gy), 3)
            # draw player
            px_mm = int((px - min_x) * scale)
            py_mm = int((py - min_y) * scale)
            pygame.draw.circle(screen, (30, 144, 255), (mm_x + px_mm, mm_y + py_mm), 4)
        except Exception:
            pass

        # reading UI
        if mode == 'reading' and read_lines:
            box_h = 300
            box_w = 700
            box_x = 50
            box_y = 120
            pygame.draw.rect(screen, (20, 20, 40, 220), (box_x - 4, box_y - 4, box_w + 8, box_h + 8))
            pygame.draw.rect(screen, (240, 240, 240), (box_x, box_y, box_w, box_h))
            # render lines with scroll
            y = box_y + 10 - scroll_y
            for line in read_lines:
                img = font.render(line, True, (10, 10, 10))
                screen.blit(img, (box_x + 10, y))
                y += 22
            # hint
            hint = font.render('Use UP/DOWN to scroll, SPACE to finish', True, (80, 80, 80))
            screen.blit(hint, (box_x + 10, box_y + box_h - 30))

        # guardian question UI
        if (mode == 'guard_question' or mode == 'guard_question_results') and g_questions:
            box_h = 320
            box_w = 720
            box_x = 40
            box_y = 80
            pygame.draw.rect(screen, (30, 30, 60), (box_x - 4, box_y - 4, box_w + 8, box_h + 8))
            pygame.draw.rect(screen, (250, 250, 250), (box_x, box_y, box_w, box_h))
            # current question
            q = g_questions[g_q_index]
            qtxt = big_font.render(f"Q{g_q_index+1}: {q['question']}", True, (10, 10, 10))
            screen.blit(qtxt, (box_x + 10, box_y + 10))
            # choices
            for i, choice in enumerate(g_choices[g_q_index]):
                prefix = str(i+1) + ') '
                sel = g_selected[g_q_index] == i
                # default text color
                col = (40, 40, 40)
                # before evaluation: highlight selection in a blue tint
                if mode == 'guard_question' and sel:
                    bg = pygame.Surface((box_w - 40, 28))
                    # light-blue background and dark-blue text for the selected option
                    bg.fill((180, 210, 255))
                    screen.blit(bg, (box_x + 20, box_y + 60 + i * 30 - 2))
                    col = (10, 40, 140)

                # if the current question has been evaluated, mark correct/incorrect immediately
                try:
                    answered = (g_results and g_results[g_q_index] is not None)
                except Exception:
                    answered = False
                if answered or (mode == 'guard_question_results' and g_results):
                    # determine correct choice index for this question
                    correct_index = None
                    ans = q.get('answer')
                    for ci, ch in enumerate(g_choices[g_q_index]):
                        if str(ch).strip().lower() == str(ans).strip().lower():
                            correct_index = ci
                            break
                    # correct choice: green background
                    if correct_index is not None and i == correct_index:
                        bg = pygame.Surface((box_w - 40, 28))
                        bg.fill((200, 255, 200))
                        screen.blit(bg, (box_x + 20, box_y + 60 + i * 30 - 2))
                        col = (0, 120, 0)
                    # chosen but wrong: red background
                    elif g_selected[g_q_index] == i and (g_results and not g_results[g_q_index]):
                        bg = pygame.Surface((box_w - 40, 28))
                        bg.fill((255, 200, 200))
                        screen.blit(bg, (box_x + 20, box_y + 60 + i * 30 - 2))
                        col = (160, 0, 0)
                    else:
                        # non-relevant choices are muted
                        col = (100, 100, 100)

                txt = font.render(prefix + choice, True, col)
                screen.blit(txt, (box_x + 20, box_y + 60 + i * 30))
            hint = font.render('1/2/3 select, ←/→ nav, SPACE confirm', True, (80, 80, 80))
            screen.blit(hint, (box_x + 10, box_y + box_h - 30))

    # handle results timer and exit when in results mode
        if mode == 'guard_question_results':
            result_timer += dt
            # allow user to press SPACE to close immediately
            # after 3 seconds auto-close
            if result_timer > 3.0:
                mode = 'play'
                g_questions = []
                g_choices = []
                g_selected = []
                g_results = []
                g_q_index = 0

        # completion: if there are no more undefeated guardians, show message
        if not show_completion:
            remaining = len([g for g in guardians if not g.defeated])
            if remaining == 0:
                show_completion = True
                completion_timer = 0.0
                print('[game] player answered all guardians')

        if show_completion:
            completion_timer += dt
            # render a centered completion message
            cm_txt = big_font.render('Você respondeu todos os guardiões! Parabéns!', True, (255, 220, 0))
            cm_sub = font.render(f'Score final: {player_score}  |  Max possível: {max_possible}', True, (200, 200, 200))
            cx = (WIDTH - cm_txt.get_width()) // 2
            cy = (HEIGHT - cm_txt.get_height()) // 2 - 20
            screen.blit(cm_txt, (cx, cy))
            screen.blit(cm_sub, (cx, cy + 40))
            # after showing for 6 seconds, keep on screen but stop spawning further guardians
            if completion_timer > 6.0:
                # prevent further spawns by setting a flag; spawn_guardians will check this
                pass

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
