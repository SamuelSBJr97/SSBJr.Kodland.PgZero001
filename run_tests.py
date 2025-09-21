#!/usr/bin/env python3
"""
Script para executar todos os testes do projeto
"""

import sys
import subprocess
import os

def run_tests():
    """Executa todos os testes do projeto"""
    
    print("🧪 Executando testes do PyGame Zero Game...")
    print("=" * 50)
    
    # Verificar se o pytest está instalado
    try:
        import pytest
    except ImportError:
        print("❌ pytest não encontrado. Instale as dependências de desenvolvimento:")
        print("pip install -r requirements-dev.txt")
        return 1
    
    # Comandos de teste
    test_commands = [
        # Testes unitários
        ["python", "-m", "pytest", "tests/unit/", "-v", "-m", "unit"],
        
        # Testes de integração
        ["python", "-m", "pytest", "tests/integration/", "-v", "-m", "integration"],
        
        # Todos os testes com cobertura
        ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=html", "--cov-report=term"],
    ]
    
    for i, cmd in enumerate(test_commands):
        print(f"\n📋 Executando comando {i+1}/{len(test_commands)}:")
        print(" ".join(cmd))
        print("-" * 30)
        
        try:
            result = subprocess.run(cmd, check=True, cwd=os.path.dirname(__file__))
        except subprocess.CalledProcessError as e:
            print(f"❌ Falha ao executar testes: {e}")
            return 1
        except FileNotFoundError:
            print("❌ Python não encontrado no PATH")
            return 1
    
    print("\n✅ Todos os testes executados com sucesso!")
    print("\n📊 Relatório de cobertura gerado em: htmlcov/index.html")
    return 0

def run_specific_tests():
    """Executa testes específicos baseado em argumentos"""
    
    if len(sys.argv) < 2:
        return run_tests()
    
    test_type = sys.argv[1].lower()
    
    if test_type == "unit":
        cmd = ["python", "-m", "pytest", "tests/unit/", "-v"]
    elif test_type == "integration":
        cmd = ["python", "-m", "pytest", "tests/integration/", "-v"]
    elif test_type == "coverage":
        cmd = ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=html"]
    elif test_type == "fast":
        cmd = ["python", "-m", "pytest", "tests/", "-v", "-m", "not slow"]
    else:
        print("❌ Tipo de teste inválido. Use: unit, integration, coverage, ou fast")
        return 1
    
    print(f"🧪 Executando testes: {test_type}")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Testes executados com sucesso!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha ao executar testes: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_specific_tests()
    sys.exit(exit_code)