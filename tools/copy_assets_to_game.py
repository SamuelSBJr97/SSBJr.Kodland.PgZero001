"""Copia os assets gerados em tools/assets para src/game/assets."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SRC_ASSETS = ROOT / 'tools' / 'assets'
DST = ROOT / 'src' / 'game' / 'assets'
DST.mkdir(parents=True, exist_ok=True)

for p in SRC_ASSETS.glob('*.png'):
    shutil.copy2(p, DST / p.name)
    print('copied', p.name)

print('All copied to', DST)
