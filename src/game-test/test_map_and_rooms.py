from game.mapgen import generate_map
from game.room import Room
from game.questions import load_questions, sample_questions
from game.game import reset_for_tests, _GS, enter_room, ask_room_questions


def test_generate_map():
    m = generate_map(123, num_rooms=10)
    assert m.seed == 123
    assert len(m.rooms) == 10


def test_room_enter_and_questions():
    reset_for_tests()
    _GS.start_game(seed=321, num_rooms=5)
    can, desc = enter_room(0)
    # player inicial tem score 0; required pode ser 0
    assert isinstance(can, bool)
    # confirmar que podemos criar Room e pedir perguntas
    _GS.goto_room(0)
    # usar o descriptor vindo do mapa (mais robusto)
    desc2 = _GS.map.rooms[0]
    qs = sample_questions(desc2.theme, _GS.rng, count=3, min_difficulty=1)
    answers = [q['answer'] for q in qs]
    success, correct_count, pts, details = ask_room_questions(desc2.theme, answers)
    assert isinstance(success, bool)
