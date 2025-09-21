#!/usr/bin/env python3
"""
Script de validação do ambiente PyGame Zero
"""

import sys
import os

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    
    print("🔍 Verificando ambiente PyGame Zero...")
    print("=" * 50)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar dependências
    dependencies = [
        ('pgzero', 'PyGame Zero'),
        ('pygame', 'PyGame'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow')
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}: Instalado")
        except ImportError:
            print(f"❌ {name}: NÃO instalado")
            missing_deps.append(name)
    
    # Verificar arquivos do jogo
    print("\n📁 Verificando arquivos do jogo...")
    required_files = [
        'src/main.py',
        'src/settings.py',
        'src/images/player.png',
        'src/images/enemy.png',
        'src/images/collectible.png'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: Encontrado")
        else:
            print(f"❌ {file_path}: NÃO encontrado")
            missing_files.append(file_path)
    
    # Relatório final
    print("\n" + "=" * 50)
    if not missing_deps and not missing_files:
        print("🎉 Ambiente configurado corretamente!")
        print("🎮 O jogo está pronto para ser executado!")
        return True
    else:
        print("⚠️  Problemas encontrados:")
        
        if missing_deps:
            print(f"📦 Dependências faltando: {', '.join(missing_deps)}")
            print("   Solução: pip install -r requirements.txt")
        
        if missing_files:
            print(f"📁 Arquivos faltando: {', '.join(missing_files)}")
            print("   Solução: Execute o script de criação de sprites")
        
        return False

def create_missing_sprites():
    """Cria sprites básicos se estiverem faltando"""
    
    print("\n🎨 Criando sprites básicos...")
    
    try:
        import pygame
        pygame.init()
        
        os.makedirs('src/images', exist_ok=True)
        
        # Sprites básicos
        sprites = [
            ('player.png', (32, 32), (0, 100, 255)),    # Azul
            ('enemy.png', (32, 32), (255, 50, 50)),     # Vermelho
            ('collectible.png', (24, 24), (255, 255, 0)) # Amarelo
        ]
        
        for filename, size, color in sprites:
            surface = pygame.Surface(size)
            surface.fill(color)
            pygame.image.save(surface, f'src/images/{filename}')
            print(f"✅ Criado: {filename}")
        
        print("🎨 Sprites criados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar sprites: {e}")
        return False

def main():
    """Função principal"""
    
    if not check_environment():
        print("\n🔧 Tentando corrigir problemas...")
        
        # Tentar criar sprites faltando
        if not os.path.exists('src/images/player.png'):
            create_missing_sprites()
        
        # Verificar novamente
        print("\n🔍 Verificando novamente...")
        if check_environment():
            print("✅ Problemas corrigidos!")
        else:
            print("❌ Ainda há problemas. Verifique manualmente.")
            return 1
    
    print("\n🚀 Para executar o jogo, use:")
    print("   python src/main.py")
    print("   ou")
    print("   python run_game.py")
    print("   ou")
    print("   run_game.bat (Windows)")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    input("\nPressione Enter para sair...")
    sys.exit(exit_code)