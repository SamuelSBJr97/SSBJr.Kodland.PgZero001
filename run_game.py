"""
Script alternativo para executar o jogo PyGame Zero
"""

import subprocess
import sys
import os

def run_game():
    """Executa o jogo PyGame Zero"""
    
    print("🎮 Iniciando PyGame Zero Game...")
    print("=" * 50)
    
    # Definir comandos possíveis para executar o jogo
    commands = [
        # Método 1: Usar python -m pgzero (mais confiável)
        [sys.executable, "-m", "pgzero", "src/main_simple.py"],
        
        # Método 2: Usar pgzrun diretamente (se estiver no PATH)
        ["pgzrun", "src/main_simple.py"],
        
        # Método 3: Executar versão pygame pura
        [sys.executable, "src/main_pygame.py"],
    ]
    
    for i, cmd in enumerate(commands):
        print(f"\n🔧 Tentativa {i+1}: {' '.join(cmd)}")
        
        try:
            # Tentar executar o comando
            result = subprocess.run(cmd, check=True, cwd=os.path.dirname(__file__))
            
            print("✅ Jogo executado com sucesso!")
            return 0
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Falha no comando: {e}")
            continue
            
        except FileNotFoundError:
            print(f"❌ Comando não encontrado: {cmd[0]}")
            continue
    
    # Se chegou aqui, nenhum método funcionou
    print("\n❌ Não foi possível executar o jogo com nenhum método!")
    print("\n💡 Soluções:")
    print("1. Certifique-se de que o ambiente virtual está ativo")
    print("2. Instale as dependências: pip install -r requirements.txt")
    print("3. Tente executar manualmente:")
    print("   python -m pgzero src/main_simple.py")
    print("   ou")
    print("   python src/main_pygame.py")
    
    return 1

def check_environment():
    """Verifica se o ambiente está configurado"""
    
    print("🔍 Verificando ambiente...")
    
    # Verificar se os arquivos existem
    required_files = [
        "src/main_simple.py",
        "src/main_pygame.py",
        "src/settings.py",
        "src/images/player.png",
        "src/images/enemy.png",
        "src/images/collectible.png"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {', '.join(missing_files)}")
        print("💡 Execute: python validate_setup.py")
        return False
    
    # Verificar dependências
    try:
        import pgzero
        import pygame
        print("✅ Dependências OK")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("🎮 PyGame Zero Game Launcher")
    print("=" * 30)
    
    if not check_environment():
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    exit_code = run_game()
    
    if exit_code != 0:
        print("\n❌ Falha ao executar o jogo")
        input("Pressione Enter para sair...")
    
    sys.exit(exit_code)