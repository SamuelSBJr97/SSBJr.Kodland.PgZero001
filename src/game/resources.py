"""Carregamento de recursos (stub para testes).

Em runtime com pgzero, você carregaria imagens/sons; aqui apenas abstraímos para teste.
"""
from pathlib import Path

from .settings import ASSETS_DIR


def get_asset_path(name: str) -> Path:
    """Retorna o caminho para um asset dentro de pasta `assets` (não garante existência)."""
    root = Path(__file__).resolve().parent
    return root / ASSETS_DIR / name


def list_assets():
    root = Path(__file__).resolve().parent / ASSETS_DIR
    if not root.exists():
        return []
    return [p.name for p in root.iterdir() if p.is_file()]
