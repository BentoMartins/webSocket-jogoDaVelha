from dataclasses import dataclass, field
from typing import Optional, Any

@dataclass(frozen=True)
class GameState:
    """Representação imutável do estado de uma partida de Jogo da Velha."""
    board: list[list[Optional[str]]] = field(
        default_factory=lambda: [[None, None, None] for _ in range(3)]
    )
    current_turn: str = "X"
    winner: Optional[str] = None
    game_over: bool = False
    player_x_id: Optional[str] = None
    player_o_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Converte o estado para um dicionário serializável."""
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "game_over": self.game_over,
            "player_x": {"symbol": "X", "active": self.player_x_id is not None},
            "player_o": {"symbol": "O", "active": self.player_o_id is not None},
        }