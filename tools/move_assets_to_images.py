"""Move assets from src/game/assets to src/game/images for pgzero Actor loading."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'game' / 'assets'
DST = ROOT / 'src' / 'game' / 'images'
DST.mkdir(parents=True, exist_ok=True)

for p in SRC.glob('*.png'):
    shutil.copy2(p, DST / p.name)
    print('moved', p.name)

print('All assets moved to', DST)
