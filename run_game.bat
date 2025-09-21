@echo off
echo 🎮 PyGame Zero Game Launcher
echo ===========================

:: Verificar se o ambiente virtual existe
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute: python -m venv .venv
    echo 💡 Depois: .venv\Scripts\activate
    echo 💡 E então: pip install -r requirements.txt
    pause
    exit /b 1
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

:: Verificar se sprites existem
if not exist "src\images\player.png" (
    echo ⚠️  Sprites não encontrados, criando...
    python validate_setup.py
)

:: Tentar diferentes métodos de execução
echo 🎮 Iniciando jogo...
echo.

echo 📋 Método 1: PyGame Zero nativo
.venv\Scripts\python.exe -m pgzero src\main_simple.py
if not errorlevel 1 goto success

echo.
echo 📋 Método 2: Versão PyGame pura
.venv\Scripts\python.exe src\main_pygame.py
if not errorlevel 1 goto success

echo.
echo 📋 Método 3: Script launcher
python run_game.py
if not errorlevel 1 goto success

:error
echo.
echo ❌ Erro ao executar o jogo
echo 💡 Soluções:
echo    1. Certifique-se de que as dependências estão instaladas
echo       pip install -r requirements.txt
echo    2. Execute python validate_setup.py para diagnóstico
echo    3. Tente executar manualmente:
echo       python -m pgzero src\main_simple.py
echo.
pause
exit /b 1

:success
echo.
echo 🎯 Jogo finalizado com sucesso!
pause
exit /b 0