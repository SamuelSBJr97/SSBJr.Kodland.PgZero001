# Projeto base para jogo com Pygame Zero

Este diretório contém uma base mínima para iniciar um jogo com Pygame Zero (pgzero).

Estrutura:
- `.venv/` - diretório placeholder para o ambiente virtual (não criado automaticamente pelo repo).
- `requirements.txt` - dependências: `pgzero`, `pygame`, `pytest`.
- `game/` - código do jogo (módulo `game`).
- `game-test/` - testes pytest para o módulo do jogo.

Como usar (Windows PowerShell):

1) Criar e ativar um ambiente virtual dentro de `src`:

```powershell
python -m venv src\.venv
.\src\.venv\Scripts\Activate.ps1
```

2) Instalar dependências:

```powershell
pip install -r src\requirements.txt
```

3) Rodar os testes:

```powershell
python -m pytest -q src\game-test
```

4) Rodar o jogo com pgzrun (após ativar o venv):

```powershell
# A partir do diretório src
pgzrun game\game.py
```

Notas:
- O módulo `game.game` fornece um fallback seguro para permitir execução dos testes mesmo se o `pgzero` não estiver presente.
- Ajuste WIDTH/HEIGHT e implemente atores e lógica de jogo em `src/game/game.py`.
