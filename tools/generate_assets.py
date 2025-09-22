"""Gera assets placeholder (PNG) simples usando Pillow.

Cria:
- tools/assets/floor.png (64x64)
- tools/assets/wall.png (64x64)
- tools/assets/player.png (32x32)
- tools/assets/book.png (32x32)
"""
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# floor
w = 64
h = 64
im = Image.new('RGBA', (w, h), (200, 200, 200, 255))
d = ImageDraw.Draw(im)
# draw grid
for x in range(0, w, 16):
    d.line([(x, 0), (x, h)], fill=(180, 180, 180, 255))
for y in range(0, h, 16):
    d.line([(0, y), (w, y)], fill=(180, 180, 180, 255))
im.save(OUT / 'floor.png')

# wall
im = Image.new('RGBA', (w, h), (120, 120, 120, 255))
d = ImageDraw.Draw(im)
d.rectangle([(8, 8), (w-8, h-8)], outline=(90, 90, 90, 255), width=3)
im.save(OUT / 'wall.png')

# player
pw = 32
ph = 32
im = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.ellipse([(2, 2), (pw-3, ph-3)], fill=(30, 144, 255, 255), outline=(0,0,0,255))
im.save(OUT / 'player.png')

# book
im = Image.new('RGBA', (pw, ph), (0,0,0,0))
d = ImageDraw.Draw(im)
d.rectangle([(4, 6), (pw-4, ph-6)], fill=(255, 215, 0, 255), outline=(120,80,0,255))
# spine line
d.line([(8, 6), (8, ph-6)], fill=(160, 110, 0, 255), width=2)
im.save(OUT / 'book.png')

print('Assets gerados em', OUT)
