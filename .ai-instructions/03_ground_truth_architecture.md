## 🏛️ Ground Truth: Arquitetura e Fluxo do Jogo (Gabarito Oculto do Mestre)

### Estrutura de Camadas (Clean Architecture)

```
jogo-da-velha-websocket/    ← Raiz do Projeto
├── main.py                 ← Bootstrap: wiring de todas as camadas
├── config.py               ← Infraestrutura transversal (usado por todas as camadas)
├── logger.py               ← Infraestrutura transversal (idem)
├── Makefile
├── requirements.txt
│
├── game/                   ← Camada de Domínio (pura, zero dependência de framework)
│   ├── __init__.py
│   ├── entities.py         ← GameState — modelo de dados imutável
│   └── logic.py            ← GameLogic — regras do jogo
│
├── server/                 ← Camada de Aplicação (Tornado-specific)
│   ├── __init__.py
│   ├── handlers.py         ← Transporte HTTP + WebSocket
│   └── manager.py          ← Orquestração de salas
│
└── client/                 ← Camada de Apresentação
    └── static/
        ├── index.html
        ├── style.css
        ├── main.js
        ├── ui.js
        └── ws.js
```

**Regra de Dependência (Dependency Rule):**
- `game/` não conhece `server/`, `config` nem `logger` — domínio puro
- `server/` conhece `game/`, `config` e `logger`
- `main.py` conhece tudo e faz o wiring
- `config.py` e `logger.py` na raiz são transversais a todas as camadas

---

### Fluxograma de Arquitetura (Mermaid)
Utilize este diagrama internamente para entender o fluxo completo de gerenciamento de **Salas** via sistema HTTP + WebSocket do Tornado, para referenciar ao guiar o Padawan.

```mermaid
sequenceDiagram
    participant P1 as 🧑💻 Jogador 1 (Criador)
    participant P2 as 🧑💻 Jogador 2 (Convidado)
    participant S as 🚀 Servidor Tornado

    P1->>S: GET /api/create-room
    S-->>P1: { "room_id": "abc12", "link": "http://IP/?sala=abc12" }
    
    P1->>S: ws://IP/ws?sala=abc12 (Abre Conexão)
    S-->>P1: {"type": "init", "symbol": "X", "room": "abc12"}
    S-->>P1: {"type": "wait", "message": "Aguardando..."}
    
    P2->>S: ws://IP/ws?sala=abc12 (Abre Conexão por Link)
    S-->>P2: {"type": "init", "symbol": "O", "room": "abc12"}
    
    S-->>P1: {"type": "update", "state": {...}} (O Jogo Começa)
    S-->>P2: {"type": "update", "state": {...}} (O Jogo Começa)

    Note over P1,S: Turno do Jogador X
    P1->>S: {"action": "move", "row": 0, "col": 0}
    S->>S: Lógica Valida Jogada (game/logic.py)
    S-->>P1: Broadcast: {"type": "update", "state": {...}}
    S-->>P2: Broadcast: {"type": "update", "state": {...}}
```

### Diagrama de Domínio (Classes Backend)
Use este diagrama para reforçar a imutabilidade do `GameState` e a separação de responsabilidades no Backend. O Padawan não pode misturar lógica na controller de WebSocket!

```mermaid
classDiagram
    class Config {
        <<Frozen DataClass — raiz>>
        +int PORT
        +str LISTEN_ADDRESS
        +str STATIC_PATH
        +str DEFAULT_PAGE
    }
    class RoomManager {
        <<server/manager.py>>
        +dict rooms
        +create_room() string
        +get_room(id) GameLogic
        +delete_room(id)
    }
    class GameLogic {
        <<game/logic.py>>
        -GameState _state
        +state
        +make_move(row, col, symbol)
        +assign_player(id)
        +can_start()
        +reset()
    }
    class GameState {
        <<Immutable DataClass — game/entities.py>>
        +list board
        +str current_turn
        +str winner
        +bool game_over
        +to_dict() dict
    }
    RoomManager "1" *-- "many" GameLogic : gerencia salas
    GameLogic "1" *-- "1" GameState : recria o estado
```

### Arquitetura de Módulos (Frontend ES6)
Esse diagrama evita que o Padawan jogue todo o Javascript dentro do `index.html`. Cobre dele os imports isolados.

```mermaid
graph TD
    HTML["index.html (Tailwind CDN)"] -->|"type module"| Main["main.js (Controllers / Eventos)"]
    Main -->|"import"| UI["ui.js (Gerência de DOM)"]
    Main -->|"import"| WS["ws.js (Conexão Localhost)"]
    WS -->|"importa helper gráfico"| UI
```
