"""Standalone pygame runner to force a visible window and draw the map + player.

Use arrow keys to move. Loads images from src/game/images if available.
"""
import pygame
import random
from pathlib import Path
import sys
import textwrap
import json

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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Run Game (pygame standalone) - Books & Guardians')
    clock = pygame.time.Clock()

    # helper: add rooms adjacent to existing rooms (up/down/left/right)
    def add_adjacent_room(base_room=None, max_tries=12):
        # choose a set of base rooms to try; if none exist, use a center base
        bases = [base_room] if base_room else (rooms.copy() if rooms else [])
        if not bases:
            bases = [{'x': WIDTH//2-100, 'y': HEIGHT//2-60, 'w':200, 'h':120}]

        # try each base room and each direction deterministically to avoid overlap
        w = random.randint(160, 300)
        h = random.randint(120, 240)
        gap = 8
        tried = []
        for base in random.sample(bases, len(bases)):
            for dir in ['right', 'left', 'down', 'up']:
                if dir == 'up':
                    x = base['x'] + (base['w'] - w)//2 + random.randint(-20, 20)
                    y = base['y'] - h - gap
                elif dir == 'down':
                    x = base['x'] + (base['w'] - w)//2 + random.randint(-20, 20)
                    y = base['y'] + base['h'] + gap
                elif dir == 'left':
                    x = base['x'] - w - gap
                    y = base['y'] + (base['h'] - h)//2 + random.randint(-20, 20)
                else:  # right
                    x = base['x'] + base['w'] + gap
                    y = base['y'] + (base['h'] - h)//2 + random.randint(-20, 20)
                # clamp to screen
                x = max(0, min(WIDTH - w - 10, x))
                y = max(40, min(HEIGHT - h - 10, y))
                newr = {'x': x, 'y': y, 'w': w, 'h': h}
                tried.append((base, dir, newr))
                # check overlap
                nr = pygame.Rect(newr['x'], newr['y'], newr['w'], newr['h'])
                overlap = False
                for ex in rooms:
                    er = pygame.Rect(ex['x'], ex['y'], ex['w'], ex['h'])
                    if nr.colliderect(er):
                        overlap = True
                        break
                if not overlap:
                    rooms.append(newr)
                    print(f'[spawn] added room adjacent ({dir}) at ({x},{y},{w},{h})')
                    return newr

        # if all adjacency attempts failed, try a few random placements near random bases
        for attempt in range(max_tries):
            base = random.choice(bases)
            x = base['x'] + random.randint(-base['w']//2, base['w'])
            y = base['y'] + random.randint(-base['h']//2, base['h'])
            x = max(0, min(WIDTH - w - 10, x))
            y = max(40, min(HEIGHT - h - 10, y))
            newr = {'x': x, 'y': y, 'w': w, 'h': h}
            nr = pygame.Rect(newr['x'], newr['y'], newr['w'], newr['h'])
            overlap = any(nr.colliderect(pygame.Rect(ex['x'], ex['y'], ex['w'], ex['h'])) for ex in rooms)
            if not overlap:
                rooms.append(newr)
                print(f'[spawn] added room near base (fallback) at ({x},{y},{w},{h})')
                return newr

        # final fallback: append overlapping room
        rooms.append(newr)
        print(f'[spawn] added room (final fallback) at ({newr["x"]},{newr["y"]},{newr["w"]},{newr["h"]})')
        return newr

    def add_rooms(n):
        for _ in range(n):
            base = random.choice(rooms) if rooms else None
            add_adjacent_room(base_room=base)

    def spawn_guardians(n, pick_rooms=None):
        # spawn n guardians, selecting rooms from pick_rooms or random existing rooms
        for i in range(n):
            if pick_rooms:
                r = random.choice(pick_rooms)
            else:
                if rooms:
                    r = random.choice(rooms)
                else:
                    # fallback: spawn near center
                    r = {'x': WIDTH//2 - 100, 'y': HEIGHT//2 - 50, 'w': 200, 'h': 120}
            gx = r['x'] + r['w']//2 + random.randint(-20, 20)
            gy = r['y'] + r['h']//2 + random.randint(-20, 20)
            # questions from sample; required score scales slightly
            q = make_sample_questions()
            req = max(0, player_score)
            newg = Guardian(gx, gy, required_score=req, questions=q)
            guardians.append(newg)
            print(f'[spawn] guardian at ({gx},{gy}) in room ({r["x"]},{r["y"]})')

    floor = load_image('floor.png', fallback_color=(200, 200, 200), size=(64, 64))
    wall = load_image('wall.png', fallback_color=(120, 120, 120), size=(64, 64))
    player_img = load_image('player.png', fallback_color=(30, 144, 255), size=(32, 32))
    book_img = load_image('book.png', fallback_color=(255, 215, 0), size=(32, 32))

    rooms = [
        {'x': 100, 'y': 80, 'w': 200, 'h': 140},
        {'x': 420, 'y': 100, 'w': 240, 'h': 160},
        {'x': 200, 'y': 320, 'w': 360, 'h': 200},
    ]

    # load game.json if present
    GAME_JSON = ROOT / 'src' / 'game' / 'game.json'
    books = []
    guardians = []
    if GAME_JSON.exists():
        try:
            with open(GAME_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # create book objects from placements linking to book definitions
            book_defs = {b['id']: b for b in data.get('books', [])}
            for p in data.get('placements', {}).get('books', []):
                bid = p.get('book_id')
                bd = book_defs.get(bid)
                text = bd.get('text') if bd else 'Sem texto.'
                points = bd.get('points', 1) if bd else 1
                books.append(Book(p.get('x', 0), p.get('y', 0), text=text, points=points))
            # guardians
            for g in data.get('guardians', []):
                guardians.append(Guardian(g.get('x', 0), g.get('y', 0), required_score=g.get('required_score', 0), questions=g.get('questions', [])))
        except Exception:
            # fallback to defaults below
            books = [
                Book(140, 110, text='Este é um livro sobre somas. Leia até o fim para ganhar 2 pontos.' , points=2),
                Book(460, 140, text='Livro: Introdução ao Python. Leia para ganhar 3 pontos.', points=3),
                Book(260, 360, text='Livro de lógica. Chegue ao fim para 2 pontos.', points=2),
            ]
            guardians = [
                Guardian(280, 200, required_score=2, questions=make_sample_questions()),
                Guardian(520, 380, required_score=4, questions=make_sample_questions()),
            ]
    else:
        books = [
            Book(140, 110, text='Este é um livro sobre somas. Leia até o fim para ganhar 2 pontos.' , points=2),
            Book(460, 140, text='Livro: Introdução ao Python. Leia para ganhar 3 pontos.', points=3),
            Book(260, 360, text='Livro de lógica. Chegue ao fim para 2 pontos.', points=2),
        ]
        guardians = [
            Guardian(280, 200, required_score=2, questions=make_sample_questions()),
            Guardian(520, 380, required_score=4, questions=make_sample_questions()),
        ]

    px, py = WIDTH // 2, HEIGHT // 2
    speed = 240

    player_score = 0

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
    g_selected = []
    g_q_index = 0
    g_results = []  # None until evaluated, then True/False per question

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
                                if player_score < g.required_score:
                                    # show temporary message by starting a short reading-like message
                                    mode = 'reading'
                                    active_book = None
                                    read_lines = [f'Você precisa de {g.required_score} pontos para conversar com o guardião.']
                                    scroll_y = 0
                                else:
                                    # start questions
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
                                if correct == len(g_questions) and active_guardian is not None:
                                    active_guardian.defeated = True
                                    player_score += 2
                                    print(f'[guard] guardian at ({active_guardian.x},{active_guardian.y}) defeated')
                                    # when a guardian is defeated, spawn one extra guardian
                                    spawn_guardians(1)
                                # when finishing a guardian questionnaire, generate 3 rooms + 2 guardians
                                add_rooms(3)
                                spawn_guardians(2)
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

        # draw background tiles
        for x in range(0, WIDTH, 64):
            for y in range(0, HEIGHT, 64):
                screen.blit(floor, (x, y))

        # draw rooms
        for r in rooms:
            pygame.draw.rect(screen, (170, 170, 170), (r['x'], r['y'], r['w'], r['h']))
            screen.blit(wall, (r['x'], r['y']))

        # draw books
        for b in books:
            if not b.read:
                screen.blit(book_img, (b.x, b.y))
            else:
                # dim read books
                s = pygame.Surface((b.w, b.h), pygame.SRCALPHA)
                s.fill((100, 100, 100, 180))
                screen.blit(s, (b.x, b.y))

        # draw guardians
        for g in guardians:
            color = (200, 50, 50) if not g.defeated else (80, 160, 80)
            pygame.draw.rect(screen, color, (g.x, g.y, g.w, g.h))

        # draw player
        screen.blit(player_img, (int(px) - 16, int(py) - 16))

        # HUD
        hud = big_font.render(f'Score: {player_score}', True, (255, 255, 255))
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

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
