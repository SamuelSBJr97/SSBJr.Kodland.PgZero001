import sys
from pathlib import Path

# Garantir que o diretório src/ (pai deste teste) esteja no sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
