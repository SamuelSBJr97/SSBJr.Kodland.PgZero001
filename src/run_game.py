"""Runner simples para o módulo `game`.

Permite executar sem problemas de import relativo (ajusta sys.path) e mostra um menu
textual básico para testar a geração de mapas e entrar em salas.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from game import game


def main():
    print(game.menu_text())
    print("Gerando mapa com seed 123 (exemplo)...")
    game.reset_for_tests()
    _gs = game._GS
    _gs.start_game(seed=123, num_rooms=10)
    print("Mapa gerado:", _gs.map)
    print("Estado:", game.get_state_snapshot())


if __name__ == '__main__':
    main()
