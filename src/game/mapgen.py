"""Gerador procedural simples de mapas com salas e corredores.

Usa uma seed para gerar reproducibilidade. Cada mapa tem `num_rooms` salas.
"""
from dataclasses import dataclass
from typing import List
import random


@dataclass
class RoomDescriptor:
    id: int
    name: str
    required_score: int
    owner_npc: str
    theme: str


@dataclass
class MapDescriptor:
    seed: int
    num_rooms: int
    rooms: List[RoomDescriptor]


def generate_map(seed: int, num_rooms: int = 10) -> MapDescriptor:
    rng = random.Random(seed)
    rooms = []
    for i in range(num_rooms):
        # dificuldade e score requerida aumenta ao longo das salas
        required = int((i / max(1, num_rooms - 1)) * 100)
        theme = rng.choice(["math", "logic", "python"])
        rooms.append(RoomDescriptor(id=i, name=f"Sala {i+1}", required_score=required, owner_npc=f"Guardiao_{i+1}", theme=theme))
    return MapDescriptor(seed=seed, num_rooms=num_rooms, rooms=rooms)
