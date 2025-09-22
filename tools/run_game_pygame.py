"""Standalone pygame runner to force a visible window and draw the map + player.

Use arrow keys to move. Loads images from src/game/images if available.
"""
import pygame
from pathlib import Path
import sys

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Run Game (pygame standalone)')
    clock = pygame.time.Clock()

    floor = load_image('floor.png', fallback_color=(200,200,200), size=(64,64))
    wall = load_image('wall.png', fallback_color=(120,120,120), size=(64,64))
    player_img = load_image('player.png', fallback_color=(30,144,255), size=(32,32))

    rooms = [
        {'x': 100, 'y': 80, 'w': 200, 'h': 140},
        {'x': 420, 'y': 100, 'w': 240, 'h': 160},
        {'x': 200, 'y': 320, 'w': 360, 'h': 200},
    ]

    px, py = WIDTH//2, HEIGHT//2
    speed = 240

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False

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
            pygame.draw.rect(screen, (170,170,170), (r['x'], r['y'], r['w'], r['h']))
            screen.blit(wall, (r['x'], r['y']))

        # draw player
        screen.blit(player_img, (int(px)-16, int(py)-16))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
