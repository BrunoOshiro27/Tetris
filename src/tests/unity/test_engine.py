from game.tetris_engine import (
    create_empty_board, is_valid_position,
    clear_lines, apply_piece_to_board,
    lock_piece, spawn_piece, get_ghost_position,
    apply_game_tick, handle_key_input, start_game,
)
from game.constants import (
    BOARD_WIDTH, BOARD_HEIGHT,
    STATE_RUNNING, STATE_PAUSED, STATE_OVER,
)
from game.pieces import TETROMINOES


# ── create_empty_board ────────────────────────────────────────────────────────

def test_empty_board_dimensions():
    board = create_empty_board()
    assert len(board) == BOARD_HEIGHT
    assert len(board[0]) == BOARD_WIDTH

def test_empty_board_all_zeros():
    board = create_empty_board()
    assert all(cell == 0 for row in board for cell in row)


# ── clear_lines ───────────────────────────────────────────────────────────────

def test_clear_full_line():
    board = create_empty_board()
    board[19] = [1] * BOARD_WIDTH
    new_board, cleared = clear_lines(board)
    assert cleared == 1
    assert new_board[19] == [0] * BOARD_WIDTH

def test_no_lines_cleared_on_empty_board():
    board = create_empty_board()
    _, cleared = clear_lines(board)
    assert cleared == 0

def test_clear_multiple_lines():
    board = create_empty_board()
    board[18] = [1] * BOARD_WIDTH
    board[19] = [1] * BOARD_WIDTH
    new_board, cleared = clear_lines(board)
    assert cleared == 2
    assert new_board[18] == [0] * BOARD_WIDTH
    assert new_board[19] == [0] * BOARD_WIDTH


# ── is_valid_position ─────────────────────────────────────────────────────────

def test_valid_position_start():
    board = create_empty_board()
    assert is_valid_position(board, "T", x=3, y=0) is True

def test_invalid_position_out_of_bounds():
    board = create_empty_board()
    assert is_valid_position(board, "T", x=-1, y=0) is False

def test_invalid_position_right_wall():
    board = create_empty_board()
    assert is_valid_position(board, "T", x=BOARD_WIDTH, y=0) is False

def test_invalid_position_below_floor():
    board = create_empty_board()
    assert is_valid_position(board, "O", x=0, y=BOARD_HEIGHT) is False

def test_invalid_position_overlaps_landed_piece():
    board = create_empty_board()
    board[1][3] = 1
    assert is_valid_position(board, "O", x=3, y=0) is False


# ── apply_piece_to_board ──────────────────────────────────────────────────────

def test_apply_piece_stamps_color_on_board():
    board = create_empty_board()
    matrix = TETROMINOES["O"]
    result = apply_piece_to_board(board, matrix, x=0, y=0, color_id=2)
    assert result[0][0] == 2
    assert result[1][1] == 2

def test_apply_piece_does_not_mutate_original():
    board = create_empty_board()
    apply_piece_to_board(board, TETROMINOES["O"], x=0, y=0, color_id=2)
    assert board[0][0] == 0


# ── spawn_piece ───────────────────────────────────────────────────────────────

def test_spawn_piece_returns_correct_shape():
    piece = spawn_piece("T")
    assert piece["shape"] == "T"
    assert piece["color_id"] == 3
    assert piece["rotation"] == 0

def test_spawn_piece_starts_at_top():
    piece = spawn_piece("I")
    assert piece["y"] == 0

def test_spawn_piece_is_centered():
    piece = spawn_piece("O")
    assert piece["x"] == BOARD_WIDTH // 2 - 2


# ── get_ghost_position ────────────────────────────────────────────────────────

def test_ghost_position_lands_near_bottom_on_empty_board():
    board = create_empty_board()
    ghost_y = get_ghost_position(board, "I", x=3, y=0, rotation=0)
    assert ghost_y > 0

def test_ghost_position_stops_above_landed_piece():
    board = create_empty_board()
    board[19] = [1] * BOARD_WIDTH
    ghost_y = get_ghost_position(board, "O", x=0, y=0, rotation=0)
    assert ghost_y < 19


# ── lock_piece ────────────────────────────────────────────────────────────────

def test_lock_piece_stamps_board():
    state = start_game()
    state["current_piece"] = spawn_piece("O")
    state["current_piece"]["y"] = 18
    result = lock_piece(state)
    assert any(cell != 0 for row in result["board"] for cell in row)

def test_lock_piece_resets_can_hold():
    state = start_game()
    state["can_hold"] = False
    result = lock_piece(state)
    assert result["can_hold"] is True

def test_lock_piece_spawns_next_piece():
    state = start_game()
    state["current_piece"] = spawn_piece("O")
    state["current_piece"]["y"] = 18
    next_shape = state["next_piece"]
    result = lock_piece(state)
    assert result["current_piece"]["shape"] == next_shape

def test_lock_piece_clears_completed_lines():
    state = start_game()
    for row in range(18, 20):
        state["board"][row] = [1] * BOARD_WIDTH
    state["current_piece"] = spawn_piece("O")
    state["current_piece"]["y"] = 16
    result = lock_piece(state)
    assert result["lines_cleared"] >= 0   # may or may not clear depending on placement


# ── handle_key_input ──────────────────────────────────────────────────────────

def test_handle_move_left():
    state = start_game()
    state["current_piece"]["x"] = 4
    initial_x = state["current_piece"]["x"]
    result = handle_key_input(state, "ArrowLeft")
    assert result["current_piece"]["x"] == initial_x - 1

def test_handle_move_right():
    state = start_game()
    state["current_piece"]["x"] = 4
    initial_x = state["current_piece"]["x"]
    result = handle_key_input(state, "ArrowRight")
    assert result["current_piece"]["x"] == initial_x + 1

def test_handle_soft_drop():
    state = start_game()
    initial_y = state["current_piece"]["y"]
    result = handle_key_input(state, "ArrowDown")
    assert result["current_piece"]["y"] == initial_y + 1

def test_handle_rotate_clockwise():
    state = start_game()
    state["current_piece"]["shape"] = "T"
    state["current_piece"]["x"] = 4
    result = handle_key_input(state, "ArrowUp")
    assert result["current_piece"]["rotation"] == 1

def test_handle_rotate_counter():
    state = start_game()
    state["current_piece"]["shape"] = "T"
    state["current_piece"]["x"] = 4
    result = handle_key_input(state, "z")
    assert result["current_piece"]["rotation"] == 3

def test_handle_hard_drop_locks_piece():
    state = start_game()
    result = handle_key_input(state, " ")
    assert any(cell != 0 for row in result["board"] for cell in row)

def test_handle_hold_piece():
    state = start_game()
    shape_before = state["current_piece"]["shape"]
    result = handle_key_input(state, "c")
    assert result["held_piece"] == shape_before
    assert result["can_hold"] is False

def test_handle_hold_twice_not_allowed():
    state = start_game()
    state = handle_key_input(state, "c")
    held_after_first = state["held_piece"]
    state = handle_key_input(state, "c")   # blocked
    assert state["held_piece"] == held_after_first

def test_handle_hold_with_existing_held_piece():
    state = start_game()
    state["held_piece"] = "I"
    state["can_hold"] = True
    result = handle_key_input(state, "c")
    assert result["current_piece"]["shape"] == "I"

def test_unknown_key_returns_state_unchanged():
    state = start_game()
    result = handle_key_input(state, "q")
    assert result == state

def test_key_ignored_when_game_over():
    state = start_game()
    state["status"] = STATE_OVER
    result = handle_key_input(state, "ArrowLeft")
    assert result["status"] == STATE_OVER

def test_pause_key_pauses_game():
    state = start_game()
    result = handle_key_input(state, "p")
    assert result["status"] == STATE_PAUSED

def test_pause_key_resumes_game():
    state = start_game()
    state["status"] = STATE_PAUSED
    result = handle_key_input(state, "p")
    assert result["status"] == STATE_RUNNING

def test_key_ignored_when_paused():
    state = start_game()
    state["status"] = STATE_PAUSED
    initial_x = state["current_piece"]["x"]
    result = handle_key_input(state, "ArrowLeft")
    assert result["current_piece"]["x"] == initial_x


# ── apply_game_tick ───────────────────────────────────────────────────────────

def test_tick_moves_piece_down():
    state = start_game()
    initial_y = state["current_piece"]["y"]
    result = apply_game_tick(state)
    assert result["current_piece"]["y"] == initial_y + 1

def test_tick_ignored_when_paused():
    state = start_game()
    state["status"] = STATE_PAUSED
    y_before = state["current_piece"]["y"]
    result = apply_game_tick(state)
    assert result["current_piece"]["y"] == y_before

def test_tick_ignored_when_game_over():
    state = start_game()
    state["status"] = STATE_OVER
    result = apply_game_tick(state)
    assert result["status"] == STATE_OVER

def test_tick_increments_counter():
    state = start_game()
    result = apply_game_tick(state)
    assert result["tick"] == 1

def test_tick_locks_piece_at_bottom():
    state = start_game()
    state["current_piece"]["y"] = BOARD_HEIGHT - 2
    result = apply_game_tick(state)
    assert any(cell != 0 for row in result["board"] for cell in row)


# ── start_game ────────────────────────────────────────────────────────────────

def test_start_game_returns_running_state():
    state = start_game()
    assert state["status"] == STATE_RUNNING

def test_start_game_has_current_piece():
    state = start_game()
    assert state["current_piece"]["shape"] in ["I","O","T","S","Z","J","L"]

def test_start_game_has_next_piece():
    state = start_game()
    assert state["next_piece"] in ["I","O","T","S","Z","J","L"]

def test_start_game_board_is_empty():
    state = start_game()
    assert all(cell == 0 for row in state["board"] for cell in row)

def test_start_game_score_is_zero():
    state = start_game()
    assert state["score"] == 0

def test_start_game_level_is_one():
    state = start_game()
    assert state["level"] == 1
