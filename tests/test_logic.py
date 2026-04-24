import pytest
from game.logic import GameLogic

def test_assign_first_player_gets_x():
    game = GameLogic()
    symbol = game.assign_player("player1")
    assert symbol == "X"

def test_assign_second_player_gets_o():
    game = GameLogic()
    game.assign_player("player1")
    symbol = game.assign_player("player2")
    assert symbol == "O"

def test_assign_third_player_returns_none():
    game = GameLogic()
    game.assign_player("player1")
    game.assign_player("player2")
    symbol = game.assign_player("player3")
    assert symbol is None

def test_is_full_with_two_players():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    assert game.is_full() is True

def test_is_full_with_one_player():
    game = GameLogic()
    game.assign_player("p1")
    assert game.is_full() is False

def test_valid_move():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    result = game.make_move(0, 0, "X")
    assert result is True
    assert game.state.board[0][0] == "X"

def test_move_out_of_bounds():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    assert game.make_move(3, 0, "X") is False

def test_move_on_occupied_cell():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.make_move(0, 0, "X")
    assert game.make_move(0, 0, "O") is False

def test_move_wrong_turn():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    assert game.make_move(0, 0, "O") is False

def test_x_wins_row():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.make_move(0, 0, "X")
    game.make_move(1, 0, "O")
    game.make_move(0, 1, "X")
    game.make_move(1, 1, "O")
    game.make_move(0, 2, "X")
    assert game.state.winner == "X"
    assert game.state.game_over is True

def test_o_wins_column():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.make_move(0, 0, "X")
    game.make_move(0, 1, "O")
    game.make_move(1, 0, "X")
    game.make_move(1, 1, "O")
    game.make_move(2, 2, "X")
    game.make_move(2, 1, "O")
    assert game.state.winner == "O"
    assert game.state.game_over is True

def test_draw():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    moves = [
        (0,0,"X"),(0,1,"O"),(0,2,"X"),
        (1,1,"O"),(1,0,"X"),(1,2,"O"),
        (2,1,"X"),(2,0,"O"),(2,2,"X"),
    ]
    for r, c, s in moves:
        game.make_move(r, c, s)
    assert game.state.winner == "Draw"
    assert game.state.game_over is True

def test_move_after_game_over():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.make_move(0, 0, "X")
    game.make_move(1, 0, "O")
    game.make_move(0, 1, "X")
    game.make_move(1, 1, "O")
    game.make_move(0, 2, "X")
    assert game.make_move(2, 2, "O") is False

def test_reset_after_x_wins():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.make_move(0, 0, "X")
    game.make_move(1, 0, "O")
    game.make_move(0, 1, "X")
    game.make_move(1, 1, "O")
    game.make_move(0, 2, "X")
    game.reset()
    assert game.state.game_over is False
    assert game.state.winner is None
    assert game.state.current_turn == "X"

def test_remove_player():
    game = GameLogic()
    game.assign_player("p1")
    game.assign_player("p2")
    game.remove_player("p1")
    assert game.is_full() is False