from game.book import default_books_for_room
from game.room import Room
from game.mapgen import generate_map
from game.game import reset_for_tests, _GS
from game.questions import sample_questions


def test_books_default_locked():
    books = default_books_for_room(1)
    assert all(b.locked for b in books)


def test_room_unlock_books_on_success():
    reset_for_tests()
    _GS.start_game(seed=99, num_rooms=3)
    _GS.goto_room(0)
    room = _GS.current_room
    theme = room.descriptor.theme
    qs = sample_questions(theme, _GS.rng, count=3)
    answers = [q['answer'] for q in qs]
    success = room.ask_questions(qs, answers)
    assert success is True
    assert all(not b.locked for b in room.books)
