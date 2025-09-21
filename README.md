# 🎮 SSBJr.Kodland.PgZero001

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![PyGame Zero](https://img.shields.io/badge/PyGame%20Zero-1.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-80%25+-orange.svg)

Um projeto de jogo educacional desenvolvido com PyGame Zero para aprendizado de desenvolvimento de jogos em Python.

## 📖 Sobre o Projeto

Este é um projeto de jogo desenvolvido utilizando **PyGame Zero**, uma biblioteca Python que facilita a criação de jogos para iniciantes. O PyGame Zero foi projetado para ser uma introdução amigável ao desenvolvimento de jogos em Python, removendo a complexidade do setup inicial e permitindo foco na lógica do jogo.

### 🎯 Objetivos do Projeto:
- Demonstrar conceitos fundamentais de desenvolvimento de jogos
- Praticar programação orientada a objetos em Python
- Implementar mecânicas básicas de jogos (movimento, colisão, pontuação)
- Aplicar boas práticas de desenvolvimento com testes automatizados

## 🛠️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

| Requisito | Versão Mínima | Descrição |
|-----------|---------------|-----------|
| **Python** | 3.6+ | Linguagem de programação principal |
| **PyGame Zero** | 1.2+ | Framework para desenvolvimento de jogos |
| **Git** | 2.0+ | Para controle de versão (opcional) |

### 🔧 Verificar Instalação:
```bash
# Verificar versão do Python
python --version

# Verificar se o PyGame Zero está instalado
python -c "import pgzero; print('PyGame Zero instalado com sucesso!')"
```

## 📥 Instalação

### 1️⃣ Clone o repositório:
```bash
git clone https://github.com/SamuelSBJr97/SSBJr.Kodland.PgZero001.git
cd SSBJr.Kodland.PgZero001
```

### 2️⃣ Crie um ambiente virtual (recomendado):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as dependências:
```bash
# Dependências básicas do jogo
pip install -r requirements.txt

# Para desenvolvimento (incluindo testes)
pip install -r requirements-dev.txt
```

### 4️⃣ Verifique a instalação:
```bash
python src/main.py
```

## 🚀 Como Executar

### 🎮 Método Principal (Recomendado):
```bash
# Ativar ambiente virtual (se não estiver ativo)
.venv\Scripts\activate    # Windows
# ou
source .venv/bin/activate # Linux/macOS

# Executar o jogo
cd src
python main.py
```

### 🐍 Método Alternativo com pgzrun:
```bash
cd src
pgzrun main.py
```

### 🎯 Scripts de Conveniência:
```bash
# Script Python (multiplataforma)
python run_game.py

# Script Windows Batch
run_game.bat

# Validar configuração do ambiente
python validate_setup.py
```

> **💡 Dica:** Se você receber erro sobre módulos não encontrados, certifique-se de que:
> 1. O ambiente virtual está ativo
> 2. As dependências foram instaladas: `pip install -r requirements.txt`
> 3. Execute `python validate_setup.py` para verificar o ambiente

## 📁 Estrutura do Projeto

```
📦 SSBJr.Kodland.PgZero001/
├── 📄 README.md                 # Documentação do projeto
├── 📄 requirements.txt          # Dependências de produção
├── 📄 requirements-dev.txt      # Dependências de desenvolvimento
├── 📄 pytest.ini              # Configurações do pytest
├── 📄 run_tests.py            # Script para executar testes
├── 📄 .gitignore              # Arquivos ignorados pelo Git
├── 📂 src/                    # Código fonte do jogo
│   ├── 🎮 main.py             # Arquivo principal do jogo
│   ├── ⚙️ settings.py         # Configurações do jogo
│   ├── 📂 images/             # Sprites e imagens
│   │   └── 📄 README.md       # Guia para imagens
│   ├── 📂 sounds/             # Efeitos sonoros
│   │   └── 📄 README.md       # Guia para sons
│   └── 📂 music/              # Música de fundo
│       └── 📄 README.md       # Guia para música
└── 📂 tests/                  # Testes automatizados
    ├── 📄 conftest.py         # Configurações de teste
    ├── 📂 unit/               # Testes unitários
    │   ├── test_settings.py   # Testes das configurações
    │   ├── test_player_movement.py  # Testes de movimento
    │   └── test_collision.py  # Testes de colisão
    └── 📂 integration/        # Testes de integração
        └── test_game_flow.py  # Testes do fluxo do jogo
```

## 📚 Sobre o PyGame Zero

### 🎯 **Por que PyGame Zero?**

PyGame Zero é uma biblioteca Python criada especificamente para **simplificar** a criação de jogos, especialmente para **iniciantes** e **educação**. 

#### ✨ **Principais Vantagens:**

| Característica | Benefício | Exemplo |
|----------------|-----------|---------|
| 🚀 **Zero Boilerplate** | Menos código inicial necessário | Sem `pygame.init()`, loops manuais |
| 🎓 **Educacional** | Foco no aprendizado de lógica | Ideal para ensino de programação |
| 🔄 **Auto-gerenciado** | Gerenciamento automático de recursos | Sprites, sons carregados automaticamente |
| 📖 **API Simples** | Sintaxe intuitiva e clara | `actor.draw()`, `keyboard.left` |
| 🎮 **Baseado no Pygame** | Toda potência do Pygame disponível | Performance e recursos avançados |

#### 🔧 **Funcionalidades Integradas:**
- ✅ **Carregamento automático** de sprites, sons e música
- ✅ **Game loop** gerenciado automaticamente
- ✅ **Sistema de eventos** simplificado
- ✅ **Detecção de colisão** built-in
- ✅ **Renderização** otimizada
- ✅ **Input handling** intuitivo

#### 🎨 **Conceitos Fundamentais:**

```python
# Exemplo da simplicidade do PyGame Zero
def draw():
    screen.fill('blue')          # Fundo azul
    player.draw()                # Desenha o jogador
    
def update():
    if keyboard.left:            # Se seta esquerda pressionada
        player.x -= 5            # Move jogador para esquerda
```

### 🌟 **Evoluindo do PyGame Zero:**
À medida que você domina o PyGame Zero, pode evoluir para:
- **Pygame** puro para controle total
- **Arcade** para jogos 2D mais complexos  
- **Godot** com Python para projetos maiores
- **Unity** com C# para desenvolvimento profissional

## 🎮 Recursos do Jogo

### 🕹️ **Mecânicas Implementadas:**
- ✅ **Sistema de Movimento** - Controle fluido do jogador com setas do teclado
- ✅ **Detecção de Colisão** - Colisões precisas entre jogador, inimigos e itens
- ✅ **Sistema de Pontuação** - Pontos ao coletar itens
- ✅ **Inimigos Dinâmicos** - Spawn automático de inimigos em intervalos
- ✅ **Coletáveis** - Itens que aparecem periodicamente para coletar
- ✅ **Game Over** - Estado de fim de jogo ao colidir com inimigos
- ✅ **Sistema de Reset** - Reiniciar o jogo a qualquer momento
- ✅ **Controles Responsivos** - Input lag mínimo e controles suaves

### 🎯 **Características Técnicas:**
- **Engine**: PyGame Zero 1.2+
- **Linguagem**: Python 3.6+
- **Padrão de Arquitetura**: Game Loop clássico
- **Sistema de Assets**: Carregamento automático de recursos
- **Performance**: 60 FPS target
- **Compatibilidade**: Windows, Linux, macOS

## 💻 Desenvolvimento

### 🔧 **Configuração do Ambiente de Desenvolvimento:**

1. **Fork e Clone** o repositório
2. **Configure um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate     # Windows
   ```
3. **Instale dependências de desenvolvimento:**
   ```bash
   pip install -r requirements-dev.txt
   ```

### 🎨 **Adicionando Recursos ao Jogo:**

#### 🖼️ **Imagens e Sprites:**
```bash
# Adicione seus sprites na pasta correta
src/images/
├── player.png          # Sprite do jogador (recomendado: 32x32px)
├── enemy.png           # Sprite do inimigo (recomendado: 32x32px)
├── collectible.png     # Sprite do coletável (recomendado: 24x24px)
└── background.png      # Fundo do jogo (800x600px)
```

#### 🔊 **Áudio:**
```bash
# Sons e músicas
src/sounds/             # Efeitos sonoros (.wav recomendado)
├── jump.wav
├── collect.wav
└── explosion.wav

src/music/              # Música de fundo (.ogg recomendado)
├── background.ogg
└── menu.ogg
```

#### ⚙️ **Configurações:**
- Modifique `src/settings.py` para ajustar:
  - Dimensões da tela
  - Velocidades de movimento
  - Cores do jogo
  - Configurações de áudio

#### 🎮 **Lógica do Jogo:**
- O arquivo principal `src/main.py` contém:
  - `draw()`: Função de renderização
  - `update()`: Lógica do jogo
  - `on_key_down()`: Tratamento de input

### 🛠️ **Ferramentas de Desenvolvimento:**

| Ferramenta | Propósito | Comando |
|------------|-----------|---------|
| **pytest** | Testes automatizados | `pytest` |
| **black** | Formatação de código | `black src/ tests/` |
| **flake8** | Linting (qualidade de código) | `flake8 src/ tests/` |
| **isort** | Organização de imports | `isort src/ tests/` |
| **mypy** | Type checking | `mypy src/` |

### 📝 **Convenções de Código:**
- Use **snake_case** para variáveis e funções
- Use **PascalCase** para classes
- Máximo de **88 caracteres** por linha
- Docstrings em **formato Google**
- Type hints quando possível

### 🔄 **Workflow de Desenvolvimento:**
1. 🌟 Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
2. 💻 Desenvolva e teste localmente
3. 🧪 Execute todos os testes: `python run_tests.py`
4. 🎨 Formate o código: `black src/ tests/`
5. 📝 Commit suas mudanças: `git commit -m "feat: adiciona nova funcionalidade"`
6. 🚀 Push e crie um Pull Request

### 🧪 **Executando Testes**

Este projeto inclui uma suíte completa de testes automatizados para garantir a qualidade e estabilidade do código.

#### 📦 **Instalação das dependências de teste:**
```bash
pip install -r requirements-dev.txt
```

#### 🚀 **Executar todos os testes:**
```bash
# Método recomendado - script personalizado
python run_tests.py

# Método direto com pytest
pytest
```

#### 🎯 **Executar tipos específicos de teste:**
```bash
# 🔬 Testes unitários apenas
python run_tests.py unit

# 🔗 Testes de integração apenas
python run_tests.py integration

# 📊 Testes com relatório de cobertura detalhado
python run_tests.py coverage

# ⚡ Testes rápidos (exclui testes marcados como lentos)
python run_tests.py fast
```

#### 🛠️ **Usando pytest diretamente:**
```bash
# Todos os testes com output verboso
pytest -v

# Testes unitários específicos
pytest tests/unit/ -v

# Testes de integração específicos
pytest tests/integration/ -v

# Testes com cobertura de código
pytest --cov=src --cov-report=html --cov-report=term

# Executar testes em paralelo (mais rápido)
pytest -n auto

# Executar apenas testes que falharam na última execução
pytest --lf
```

#### 📊 **Interpretando Relatórios:**

**Relatório de Cobertura:**
- Após executar `python run_tests.py coverage`, abra `htmlcov/index.html` no navegador
- Meta de cobertura: **80%+** 
- Linhas vermelhas = não testadas
- Linhas verdes = testadas

**Tipos de Teste:**
- 🔬 **Unit Tests**: Testam funções individuais isoladamente
- 🔗 **Integration Tests**: Testam o fluxo completo do jogo
- ⚡ **Fast Tests**: Testes rápidos para desenvolvimento ágil
- 🐌 **Slow Tests**: Testes mais demorados (simulações longas)

#### 🎯 **Estrutura de Testes:**
```
tests/
├── 📄 conftest.py              # Fixtures e configurações globais
├── 📂 unit/                    # Testes unitários
│   ├── test_settings.py        # ⚙️ Validação de configurações
│   ├── test_player_movement.py # 🕹️ Testes de movimento do jogador
│   └── test_collision.py       # 💥 Testes de colisão e lógica
└── 📂 integration/             # Testes de integração
    └── test_game_flow.py       # 🎮 Fluxo completo do jogo
```

## 🎮 Controles do Jogo

| Tecla | Ação | Descrição |
|-------|------|-----------|
| **⬅️ ➡️ ⬆️ ⬇️** | Movimento | Move o jogador em todas as direções |
| **Espaço** | Ação Principal | Ação especial (pode ser customizada) |
| **ESC** | Sair | Fecha o jogo |
| **R** | Reiniciar | Reinicia o jogo após Game Over |

### 🎯 **Dicas de Jogabilidade:**
- 🏃‍♂️ **Movimento**: Use as setas para navegar pelo campo de jogo
- 💎 **Coleta**: Colete itens para aumentar sua pontuação
- ⚠️ **Evitar**: Desvie dos inimigos para não perder o jogo
- 🔄 **Reset**: Pressione R após o Game Over para jogar novamente

## 📖 Recursos de Aprendizado

### 📚 **Documentação Oficial:**
- 🌐 [PyGame Zero Documentation](https://pygame-zero.readthedocs.io/) - Documentação completa
- 🎓 [Tutorial Oficial](https://pygame-zero.readthedocs.io/en/stable/introduction.html) - Começando do zero
- 💡 [Exemplos de Código](https://pygame-zero.readthedocs.io/en/stable/examples.html) - Projetos práticos
- 🔧 [API Reference](https://pygame-zero.readthedocs.io/en/stable/reference.html) - Referência técnica

### 🎯 **Tutoriais Recomendados:**
- 🎮 [Real Python - PyGame Zero](https://realpython.com/pygame-a-primer/) - Tutorial detalhado
- 📺 [YouTube - PyGame Zero Playlist](https://youtube.com/playlist?list=PLsk-HSGFjnaGe7DFaIhWdHl6XUh8iuNhE) - Vídeos práticos
- 📖 [Mission Python Book](https://nostarch.com/missionpython) - Livro educacional
- 🎓 [Codecademy Python Course](https://www.codecademy.com/learn/learn-python-3) - Base em Python

### 🛠️ **Ferramentas Úteis:**
| Ferramenta | Propósito | Link |
|------------|-----------|------|
| **GIMP** | Editor de imagens gratuito | [gimp.org](https://gimp.org) |
| **Aseprite** | Editor de pixel art | [aseprite.org](https://aseprite.org) |
| **Audacity** | Editor de áudio gratuito | [audacityteam.org](https://audacityteam.org) |
| **VS Code** | Editor de código | [code.visualstudio.com](https://code.visualstudio.com) |

### 🎨 **Assets Gratuitos:**
- 🖼️ [OpenGameArt.org](https://opengameart.org) - Arte e sprites gratuitos
- 🎵 [Freesound.org](https://freesound.org) - Efeitos sonoros (requer conta)
- 🎶 [Incompetech.com](https://incompetech.com) - Música (Kevin MacLeod)
- 🎨 [Kenney.nl](https://kenney.nl/assets) - Asset packs completos

### 🚀 **Próximos Passos:**
1. 📝 Complete este projeto básico
2. 🎮 Adicione suas próprias mecânicas
3. 🎨 Crie seus próprios assets
4. 🌟 Publique seu jogo no GitHub
5. 🏆 Participe de game jams

## 🛠️ Troubleshooting

### ❌ **Problemas Comuns e Soluções:**

#### **Erro: "No module named 'pgzrun'"**
```bash
# Solução: Ativar ambiente virtual e instalar dependências
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### **Erro: "No module named 'pygame'"**
```bash
# Instalar pygame manualmente
pip install pygame>=2.0.0
```

#### **Erro: "pygame.error: No available video device"**
```bash
# No Linux, instalar dependências do sistema
sudo apt-get install python3-pygame
```

#### **Sprites não encontrados**
```bash
# Executar script de validação que cria sprites básicos
python validate_setup.py
```

#### **Jogo não abre/fecha imediatamente**
- Verifique se há erros no console
- Execute `python validate_setup.py` para diagnóstico
- Certifique-se de que o ambiente virtual está ativo

### 🔧 **Scripts de Diagnóstico:**

```bash
# Validar ambiente completo
python validate_setup.py

# Verificar dependências Python
python -c "import pgzero, pygame; print('✅ Tudo OK!')"

# Testar criação de sprites
python -c "
import pygame
pygame.init()
print('Pygame versão:', pygame.version.ver)
"
```

### 📱 **Suporte por Plataforma:**

| Plataforma | Status | Notas |
|------------|--------|-------|
| **Windows 10/11** | ✅ Testado | Use PowerShell ou CMD |
| **macOS** | ✅ Compatível | Testado em macOS 10.14+ |
| **Linux Ubuntu** | ✅ Compatível | Instale dependências do sistema |
| **Linux outras** | ⚠️ Não testado | Deve funcionar com ajustes |

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Este é um projeto educacional e adoraríamos ter sua ajuda para melhorá-lo.

### 🌟 **Como Contribuir:**

1. **🍴 Fork** o projeto
2. **🌿 Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **💻 Desenvolva** sua funcionalidade
4. **✅ Teste** suas mudanças (`python run_tests.py`)
5. **📝 Commit** suas mudanças (`git commit -m 'feat: Add some AmazingFeature'`)
6. **🚀 Push** para a branch (`git push origin feature/AmazingFeature`)
7. **📬 Abra** um Pull Request

### 🎯 **Áreas que Precisam de Ajuda:**
- 🎮 Novas mecânicas de jogo
- 🎨 Melhores assets visuais
- 🔊 Efeitos sonoros e música
- 📚 Documentação e tutoriais
- 🧪 Mais testes automatizados
- 🌐 Internacionalização
- 📱 Suporte para mobile

### 📋 **Diretrizes de Contribuição:**
- ✅ Siga as convenções de código existentes
- 🧪 Adicione testes para novas funcionalidades
- 📖 Documente mudanças significativas
- 🎯 Mantenha commits focados e descritivos
- 💬 Seja respeitoso nas discussões

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 📝 **Resumo da Licença:**
- ✅ **Uso comercial** permitido
- ✅ **Modificação** permitida  
- ✅ **Distribuição** permitida
- ✅ **Uso privado** permitido
- ⚠️ **Sem garantia** fornecida
- 📄 **Atribuição** necessária

## 👤 Autor

**Samuel S. B. Jr.**

- 📧 Email: [seu-email@exemplo.com](mailto:seu-email@exemplo.com)
- 🐙 GitHub: [@SamuelSBJr97](https://github.com/SamuelSBJr97)
- 💼 LinkedIn: [Samuel S. B. Jr.](https://linkedin.com/in/seu-perfil)
- 🌐 Website: [seu-website.com](https://seu-website.com)

---

## 🙏 Agradecimentos

- 🎮 **PyGame Zero Team** - Pela incrível biblioteca
- 🎓 **Kodland** - Pela inspiração educacional
- 🌟 **Comunidade Python** - Pelo suporte contínuo
- 🎨 **OpenGameArt.org** - Pelos recursos visuais gratuitos
- 📚 **Real Python** - Pelos excelentes tutoriais

---

<div align="center">

### ⭐ **Se este projeto te ajudou, considere dar uma estrela!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/SamuelSBJr97/SSBJr.Kodland.PgZero001?style=social)](https://github.com/SamuelSBJr97/SSBJr.Kodland.PgZero001)

**Feito com ❤️ e ☕ por Samuel S. B. Jr.**

</div>