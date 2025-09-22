# Script para ativar o venv em src/.venv e facilitar rodar o jogo ou testes
param(
    [string]$mode = "run", # run | test
    [int]$seed = 42
)

$venv = Join-Path -Path (Split-Path -Parent $PSScriptRoot) -ChildPath "src\.venv\Scripts\Activate.ps1"
if (Test-Path $venv) {
    Write-Host "Ativando venv: $venv"
    & $venv
} else {
    Write-Host "Venv não encontrado em src/.venv. Crie-o com: python -m venv src/.venv"
    exit 1
}

if ($mode -eq "test") {
    Write-Host "Rodando testes..."
    python -m pytest -q src\game-test
} else {
    Write-Host "Rodando runner do jogo (texto)..."
    python src\run_game.py
}
