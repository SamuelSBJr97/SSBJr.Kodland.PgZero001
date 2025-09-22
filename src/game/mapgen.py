"""Gerador procedural simples de mapas com salas e corredores.

Usa uma seed para gerar reproducibilidade. Cada mapa tem `num_rooms` salas.
"""
from dataclasses import dataclass
from typing import List
import random
from .settings import WIDTH, HEIGHT


@dataclass
class RoomDescriptor:
    id: int
    name: str
    required_score: int
    owner_npc: str
    theme: str
    x: int
    y: int
    w: int
    h: int


@dataclass
class MapDescriptor:
    seed: int
    num_rooms: int
    rooms: List[RoomDescriptor]


def generate_map(seed: int, num_rooms: int = 10) -> MapDescriptor:
    rng = random.Random(seed)
    rooms = []
    # room sizes
    min_w, max_w = 80, 160
    min_h, max_h = 60, 140
    attempts = 0
    placed = []
    for i in range(num_rooms):
        required = int((i / max(1, num_rooms - 1)) * 100)
        theme = rng.choice(["math", "logic", "python"])
        # try to place without overlap
        for _ in range(200):
            w = rng.randint(min_w, max_w)
            h = rng.randint(min_h, max_h)
            x = rng.randint(10, max(10, WIDTH - w - 10))
            y = rng.randint(10, max(10, HEIGHT - h - 10))
            rect = (x, y, w, h)
            ok = True
            for ox, oy, ow, oh in placed:
                if not (x + w < ox or ox + ow < x or y + h < oy or oy + oh < y):
                    ok = False
                    break
            if ok:
                placed.append(rect)
                rooms.append(RoomDescriptor(id=i, name=f"Sala {i+1}", required_score=required, owner_npc=f"Guardiao_{i+1}", theme=theme, x=x, y=y, w=w, h=h))
                break
        else:
            # fallback: place overlapping
            w = rng.randint(min_w, max_w)
            h = rng.randint(min_h, max_h)
            x = rng.randint(10, max(10, WIDTH - w - 10))
            y = rng.randint(10, max(10, HEIGHT - h - 10))
            rooms.append(RoomDescriptor(id=i, name=f"Sala {i+1}", required_score=required, owner_npc=f"Guardiao_{i+1}", theme=theme, x=x, y=y, w=w, h=h))
    return MapDescriptor(seed=seed, num_rooms=num_rooms, rooms=rooms)
