@echo off
echo 🎮 PyGame Zero Game Launcher
echo ===========================

:: Verificar se o ambiente virtual existe
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute: python -m venv .venv
    pause
    exit /b 1
)

:: Ativar ambiente virtual e executar
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo 🎮 Iniciando jogo...
python src\main.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o jogo
    echo 💡 Certifique-se de que as dependências estão instaladas:
    echo    pip install -r requirements.txt
    echo.
    pause
)

echo.
echo 🎯 Jogo finalizado!
pause