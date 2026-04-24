from game.entities import GameState

class GameLogic:
    def __init__(self) -> None:
        self._state = GameState()

    @property
    def state(self) -> GameState:
        return self._state

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        if self._state.game_over:
            return False
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        if self._state.board[row][col] is not None:
            return False
        if symbol != self._state.current_turn:
            return False

        new_board = [list(r) for r in self._state.board]
        new_board[row][col] = symbol

        winner, game_over = self._check_status(new_board)

        next_turn = "O" if self._state.current_turn == "X" else "X"
        if game_over:
            next_turn = self._state.current_turn

        self._state = GameState(
            board=new_board,
            current_turn=next_turn,
            winner=winner,
            game_over=game_over,
            player_x_id=self._state.player_x_id,
            player_o_id=self._state.player_o_id,
        )
        return True

    def _check_status(self, board: list[list[str | None]]) -> tuple[str | None, bool]:
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
                return board[i][0], True
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
                return board[0][i], True
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return board[0][0], True
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return board[0][2], True
        if all(cell is not None for row in board for cell in row):
            return "Draw", True
        return None, False

    def assign_player(self, player_id: str) -> str | None:
        if self._state.player_x_id is None:
            self._state = GameState(
                board=self._state.board, current_turn=self._state.current_turn,
                winner=self._state.winner, game_over=self._state.game_over,
                player_x_id=player_id, player_o_id=self._state.player_o_id,
            )
            return "X"
        elif self._state.player_o_id is None:
            self._state = GameState(
                board=self._state.board, current_turn=self._state.current_turn,
                winner=self._state.winner, game_over=self._state.game_over,
                player_x_id=self._state.player_x_id, player_o_id=player_id,
            )
            return "O"
        return None

    def remove_player(self, player_id: str) -> None:
        player_x = self._state.player_x_id if self._state.player_x_id != player_id else None
        player_o = self._state.player_o_id if self._state.player_o_id != player_id else None
        self._state = GameState(
            board=self._state.board, current_turn=self._state.current_turn,
            winner=self._state.winner, game_over=self._state.game_over,
            player_x_id=player_x, player_o_id=player_o,
        )

    def is_full(self) -> bool:
        return self._state.player_x_id is not None and self._state.player_o_id is not None

    def can_start(self) -> bool:
        return self.is_full()

    def reset(self) -> None:
        new_turn = self._state.winner if self._state.winner in ["X", "O"] else "X"
        self._state = GameState(
            player_x_id=self._state.player_x_id,
            player_o_id=self._state.player_o_id,
            current_turn=new_turn,
        )