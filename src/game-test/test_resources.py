from game.resources import get_asset_path, list_assets
from pathlib import Path


def test_get_asset_path_returns_path():
    p = get_asset_path("foo.png")
    assert isinstance(p, Path)
    assert p.name == "foo.png"


def test_list_assets_empty_or_list():
    items = list_assets()
    assert isinstance(items, list)
