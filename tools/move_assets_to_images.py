"""Move assets from src/game/assets to src/game/images for pgzero Actor loading."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'game' / 'assets'
DST = ROOT / 'src' / 'game' / 'images'
"""Stub: move_assets_to_images is deprecated and moved to tools/unused.

This file is intentionally left as a no-op to avoid accidental execution.
"""

def main():
    print('move_assets_to_images is unused — see tools/unused for archived helpers')

if __name__ == '__main__':
    main()
    
print('All assets moved to', DST)

print('All assets moved to', DST)
