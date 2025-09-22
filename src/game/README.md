# Módulo `game`

Este diretório contém a estrutura base do jogo separada em módulos:

- `settings.py` — constantes do jogo (WIDTH, HEIGHT, FPS, ASSETS_DIR)
- `entities.py` — definições de entidade (Player, Vector2) e factory
- `resources.py` — helpers para localizar assets
- `input.py` — estado e utilitários para entrada
- `app.py` — classe `GameApp` que orquestra tudo
- `assets/` — local para imagens/sons (vazio por enquanto)

Tudo foi desenhado para permitir execução de testes sem que o `pgzero` precise estar presente no import time.
