# 🎮 Jogo da Velha — WebSocket + Tornado

Sistema multiplayer em tempo real construído com Python, Tornado e WebSockets.

## 🚀 Como executar

```bash
# Instalar dependências
make setup

# Iniciar servidor
make run

Acesse http://localhost:8888 no navegador.

🌐 Expor para a internet

# Servidor + túnel SSH (subdomínio fixo)
make dev-serveo

# Servidor + túnel SSH (URL aleatória)
make dev-lhr

# Encerrar tudo
make stop

🏗️ Arquitetura

├── core/        # Configuração e logger centralizados
├── game/        # Domínio puro (GameState imutável + GameLogic)
├── server/      # Camada Tornado (WebSocket handlers + RoomManager)
├── hardware/    # Integração Raspberry Pi (LCD + Buzzer)
└── client/      # Frontend ES6 modular (ws.js, ui.js, main.js)

 Testes

./venv/bin/pytest tests/ -v --cov=game --cov-report=term-missing
Cobertura atual: 96%

🛠️ Tecnologias
Python 3.12 + Tornado 6.5
WebSockets (RFC 6455)
HTML + Tailwind CSS + ES6 Modules
Túnel SSH reverso (serveo.net / localhost.run)