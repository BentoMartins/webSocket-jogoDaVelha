import pytest
from game.entities import GameState

def test_gamestate_initial_board():
    state = GameState()
    assert len(state.board) == 3
    assert all(len(row) == 3 for row in state.board)
    assert all(cell is None for row in state.board for cell in row)

def test_gamestate_initial_turn():
    state = GameState()
    assert state.current_turn == "X"

def test_gamestate_is_immutable():
    state = GameState()
    with pytest.raises(Exception):
        state.current_turn = "O"

def test_gamestate_to_dict():
    state = GameState()
    d = state.to_dict()
    assert "board" in d
    assert "current_turn" in d
    assert "winner" in d
    assert "game_over" in d
    assert d["player_x"]["symbol"] == "X"
    assert d["player_o"]["symbol"] == "O"

def test_gamestate_to_dict_active_players():
    state = GameState(player_x_id="p1", player_o_id="p2")
    d = state.to_dict()
    assert d["player_x"]["active"] is True
    assert d["player_o"]["active"] is True

def test_gamestate_to_dict_no_players():
    state = GameState()
    d = state.to_dict()
    assert d["player_x"]["active"] is False
    assert d["player_o"]["active"] is False