"""Lógica de sala: interação com guardião e perguntas."""
from dataclasses import dataclass
from typing import List
from .book import default_books_for_room


@dataclass
class RoomState:
    id: int
    explored: bool = False
    score_taken: int = 0
    books_unlocked: int = 0


class Room:
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.state = RoomState(id=descriptor.id)
        # cada sala tem três livros bloqueados inicialmente
        self.books = default_books_for_room(descriptor.id)

    def can_enter(self, player_score: int) -> bool:
        return player_score >= self.descriptor.required_score

    def ask_questions(self, questions: List[dict], answers: List[str]) -> bool:
        """Recebe uma lista de perguntas e as respostas do player (strings)."""
        # compara com answer field
        correct = 0
        for q, a in zip(questions, answers):
            if str(q.get("answer")).strip().lower() == str(a).strip().lower():
                correct += 1
        if correct == len(questions):
            # pega pontos equivalentes a dificuldade média
            pts = sum(q.get("difficulty", 1) for q in questions)
            self.state.explored = True
            self.state.score_taken = pts
            # desbloqueia livros proporcionalmente (aqui: todos)
            for b in self.books:
                b.locked = False
            self.state.books_unlocked = len(self.books)
            return True
        else:
            # não desbloqueia nada e retorna falso
            return False

    def info(self):
        return {
            "id": self.descriptor.id,
            "name": self.descriptor.name,
            "required_score": self.descriptor.required_score,
            "theme": self.descriptor.theme,
            "owner": self.descriptor.owner_npc,
            "explored": self.state.explored,
            "books_unlocked": self.state.books_unlocked,
        }
