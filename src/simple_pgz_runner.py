"""Minimal PGZero runner to ensure the game window appears.

Defines WIDTH, HEIGHT, draw(), update(), and on_key_down() so running
`python -m pgzero.runner src.simple_pgz_runner` opens a visible window.
"""
WIDTH = 800
HEIGHT = 600

player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 200

rooms = [
    {'x': 100, 'y': 80, 'w': 200, 'h': 140},
    {'x': 420, 'y': 100, 'w': 240, 'h': 160},
    {'x': 200, 'y': 320, 'w': 360, 'h': 200},
]

in_question = False
draw_count = 0

print('simple_pgz_runner module imported. WIDTH, HEIGHT =', WIDTH, HEIGHT)

def update(dt):
    # nothing complex here
    pass

def draw():
    try:
        global draw_count
        draw_count += 1
        if draw_count <= 3:
            print(f'draw() called #{draw_count}')
        from pgzero import screen
        screen.clear()
        # background
        screen.fill((180, 180, 200))
        # draw rooms
        for r in rooms:
            screen.draw.filled_rect((r['x'], r['y'], r['w'], r['h']), (200, 200, 200))
            screen.draw.rect((r['x'], r['y'], r['w'], r['h']), 'black')
        # draw player
        screen.draw.filled_circle((int(player_x), int(player_y)), 12, 'dodgerblue')
        screen.draw.text(f"Player: ({int(player_x)},{int(player_y)})", (10, 10))
    except Exception:
        pass

def on_key_down(key):
    global player_x, player_y
    try:
        from pgzero.keyboard import keys
        if key == keys.LEFT:
            player_x -= 16
        elif key == keys.RIGHT:
            player_x += 16
        elif key == keys.UP:
            player_y -= 16
        elif key == keys.DOWN:
            player_y += 16
    except Exception:
        pass
