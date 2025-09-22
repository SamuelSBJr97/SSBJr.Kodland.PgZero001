"""Pygame display test: opens a window for 5 seconds to verify GUI works."""
import pygame
import time

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption('Pygame Display Test')
        running = True
        start = time.time()
        while running and time.time() - start < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((50, 60, 80))
            pygame.draw.circle(screen, (200, 100, 50), (200, 150), 40)
            pygame.display.flip()
            pygame.time.delay(50)
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
