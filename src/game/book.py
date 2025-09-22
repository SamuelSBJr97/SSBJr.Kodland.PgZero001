"""Representação simples de livros e teorias contidas.

Cada sala terá 3 livros: cada livro está bloqueado até o player responder corretamente
uma das perguntas (ou até completar as três perguntas). Os livros contêm textos de
teoria que podem ser lidos pelo jogador.
"""
from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    content: str
    locked: bool = True


def default_books_for_room(room_id: int):
    return [
        Book(id=1, title=f"Teoria {room_id}-1", content="Conteúdo básico 1", locked=True),
        Book(id=2, title=f"Teoria {room_id}-2", content="Conteúdo básico 2", locked=True),
        Book(id=3, title=f"Teoria {room_id}-3", content="Conteúdo básico 3", locked=True),
    ]
