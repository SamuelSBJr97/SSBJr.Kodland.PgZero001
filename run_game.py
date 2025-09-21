"""
Script alternativo para executar o jogo sem pgzrun
"""

import pygame
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_game():
    """Executa o jogo importando e configurando o PyGame Zero"""
    try:
        # Importar o jogo
        import main
        
        # Configurar PyGame Zero
        import pgzero.runner
        pgzero.runner.prepare_mod(main)
        
        # Executar o jogo
        pgzero.runner.run_mod(main)
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 Soluções:")
        print("1. Certifique-se de que o ambiente virtual está ativo")
        print("2. Instale as dependências: pip install -r requirements.txt")
        print("3. Verifique se está no diretório correto do projeto")
        return 1
    
    except Exception as e:
        print(f"❌ Erro ao executar o jogo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    print("🎮 Iniciando PyGame Zero Game...")
    print("🔧 Configurando ambiente...")
    
    exit_code = run_game()
    if exit_code != 0:
        print("\n❌ Falha ao executar o jogo")
        input("Pressione Enter para sair...")
    
    sys.exit(exit_code)