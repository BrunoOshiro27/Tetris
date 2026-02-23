from game.constants import INITIAL_GAME_STATE, STATE_RUNNING, STATE_PAUSED
from game.tetris_engine import handle_key_input, apply_game_tick

def test_start_sets_running_state():
    state = dict(INITIAL_GAME_STATE)
    state["status"] = STATE_RUNNING
    assert state["status"] == STATE_RUNNING

def test_pause_toggles_state():
    state = dict(INITIAL_GAME_STATE)
    state["status"] = STATE_RUNNING
    result = handle_key_input(state, key="p")
    assert result["status"] == STATE_PAUSED

def test_game_tick_moves_piece_down():
    state = dict(INITIAL_GAME_STATE)
    state["status"] = STATE_RUNNING
    initial_y = state["current_piece"]["y"]
    result = apply_game_tick(state)
    assert result["current_piece"]["y"] == initial_y + 1

def test_key_left_moves_piece():
    state = dict(INITIAL_GAME_STATE)
    state["status"] = STATE_RUNNING
    initial_x = state["current_piece"]["x"]
    result = handle_key_input(state, key="ArrowLeft")
    assert result["current_piece"]["x"] == initial_x - 1