import copy
import random
import numpy as np

from game.constants import (
    BOARD_WIDTH, BOARD_HEIGHT,
    SCORE_TABLE, SPEED_INCREMENT, MIN_SPEED_MS, INITIAL_SPEED_MS,
    KEY_ACTIONS, INITIAL_GAME_STATE, PIECE_IDS,
    STATE_RUNNING, STATE_PAUSED, STATE_OVER,
)
from game.pieces import TETROMINOES

# ── Board ─────────────────────────────────────────────────────────────────────

def create_empty_board():
    return [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]


def apply_piece_to_board(board, piece_matrix, x, y, color_id):
    """Stamps the current piece onto the board permanently (when it lands)."""
    new_board = copy.deepcopy(board)
    for row_i, row in enumerate(piece_matrix):
        for col_i, cell in enumerate(row):
            if cell:
                new_board[y + row_i][x + col_i] = color_id
    return new_board


def clear_lines(board):
    """Removes full rows, returns new board and number of lines cleared."""
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    empty_rows = [([0] * BOARD_WIDTH) for _ in range(lines_cleared)]
    return empty_rows + new_board, lines_cleared

# ── Pieces ────────────────────────────────────────────────────────────────────

def get_piece_matrix(shape, rotation):
    """Returns the numpy array for a piece at a given rotation (0-3)."""
    matrix = TETROMINOES[shape]
    return np.rot90(matrix, k=-rotation)   # clockwise


def random_piece():
    return random.choice(list(TETROMINOES.keys()))


# ── Collision ─────────────────────────────────────────────────────────────────

def is_valid_position(board, piece, x, y, rotation=0):
    """Returns True if the piece can exist at (x, y) without overlap or OOB."""
    matrix = get_piece_matrix(piece, rotation)
    for row_i, row in enumerate(matrix):
        for col_i, cell in enumerate(row):
            if cell:
                new_x = x + col_i
                new_y = y + row_i
                if new_x < 0 or new_x >= BOARD_WIDTH:
                    return False
                if new_y >= BOARD_HEIGHT:
                    return False
                if new_y >= 0 and board[new_y][new_x] != 0:
                    return False
    return True


# ── Scoring ───────────────────────────────────────────────────────────────────

def calculate_score(lines, level):
    if lines == 0:
        return 0
    return SCORE_TABLE.get(lines, 0) * level


def calculate_level(lines_cleared):
    return lines_cleared // 10 + 1


def calculate_speed(level):
    speed = INITIAL_SPEED_MS - (level - 1) * SPEED_INCREMENT
    return max(speed, MIN_SPEED_MS)


# ── Ghost piece ───────────────────────────────────────────────────────────────

def get_ghost_position(board, piece, x, y, rotation):
    """Returns the y position where the piece would land if hard dropped."""
    ghost_y = y
    while is_valid_position(board, piece, x, ghost_y + 1, rotation):
        ghost_y += 1
    return ghost_y


# ── Piece actions ─────────────────────────────────────────────────────────────

def spawn_piece(shape):
    return {
        "shape": shape,
        "rotation": 0,
        "x": BOARD_WIDTH // 2 - 2,   # roughly centered
        "y": 0,
        "color_id": PIECE_IDS[shape],
    }


def lock_piece(state):
    """
    Called when a piece can't move down anymore.
    Stamps it on the board, clears lines, spawns next piece.
    """
    state = copy.deepcopy(state)
    cp = state["current_piece"]
    matrix = get_piece_matrix(cp["shape"], cp["rotation"])

    state["board"] = apply_piece_to_board(
        state["board"], matrix, cp["x"], cp["y"], cp["color_id"]
    )

    state["board"], lines = clear_lines(state["board"])
    state["lines_cleared"] += lines
    state["score"] += calculate_score(lines, state["level"])
    state["level"] = calculate_level(state["lines_cleared"])
    state["can_hold"] = True

    next_shape = state["next_piece"]
    state["current_piece"] = spawn_piece(next_shape)
    state["next_piece"] = random_piece()

    # check game over — if new piece immediately collides
    cp = state["current_piece"]
    if not is_valid_position(state["board"], cp["shape"], cp["x"], cp["y"], cp["rotation"]):
        state["status"] = STATE_OVER

    return state


# ── Keyboard input ────────────────────────────────────────────────────────────

def handle_key_input(state, key):
    """
    Takes current game state and a key string, returns updated state.
    This is what your Dash keyboard callback calls.
    """
    if state["status"] == STATE_OVER:
        return state

    action = KEY_ACTIONS.get(key)

    if action is None:
        return state

    if action == "pause":
        state = copy.deepcopy(state)
        if state["status"] == STATE_RUNNING:
            state["status"] = STATE_PAUSED
        elif state["status"] == STATE_PAUSED:
            state["status"] = STATE_RUNNING
        return state

    if state["status"] != STATE_RUNNING:
        return state

    state = copy.deepcopy(state)
    cp = state["current_piece"]

    if action == "move_left":
        if is_valid_position(state["board"], cp["shape"], cp["x"] - 1, cp["y"], cp["rotation"]):
            cp["x"] -= 1

    elif action == "move_right":
        if is_valid_position(state["board"], cp["shape"], cp["x"] + 1, cp["y"], cp["rotation"]):
            cp["x"] += 1

    elif action == "soft_drop":
        if is_valid_position(state["board"], cp["shape"], cp["x"], cp["y"] + 1, cp["rotation"]):
            cp["y"] += 1
        else:
            state = lock_piece(state)

    elif action == "hard_drop":
        cp["y"] = get_ghost_position(
            state["board"], cp["shape"], cp["x"], cp["y"], cp["rotation"]
        )
        state = lock_piece(state)

    elif action == "rotate_clockwise":
        new_rotation = (cp["rotation"] + 1) % 4
        if is_valid_position(state["board"], cp["shape"], cp["x"], cp["y"], new_rotation):
            cp["rotation"] = new_rotation

    elif action == "rotate_counter":
        new_rotation = (cp["rotation"] - 1) % 4
        if is_valid_position(state["board"], cp["shape"], cp["x"], cp["y"], new_rotation):
            cp["rotation"] = new_rotation

    elif action == "hold_piece":
        if state["can_hold"]:
            held = state["held_piece"]
            state["held_piece"] = cp["shape"]
            next_shape = held if held else state["next_piece"]
            if not held:
                state["next_piece"] = random_piece()
            state["current_piece"] = spawn_piece(next_shape)
            state["can_hold"] = False

    return state


# ── Game tick ─────────────────────────────────────────────────────────────────

def apply_game_tick(state):
    """
    Called by dcc.Interval on every tick.
    Moves the piece down by 1, or locks it if it can't move.
    """
    if state["status"] != STATE_RUNNING:
        return state

    state = copy.deepcopy(state)
    cp = state["current_piece"]

    if is_valid_position(state["board"], cp["shape"], cp["x"], cp["y"] + 1, cp["rotation"]):
        cp["y"] += 1
    else:
        state = lock_piece(state)

    state["tick"] += 1
    return state


# ── Game control ──────────────────────────────────────────────────────────────

def start_game():
    """Returns a fresh game state."""
    state = copy.deepcopy(INITIAL_GAME_STATE)
    state["board"] = create_empty_board()
    state["current_piece"] = spawn_piece(random_piece())
    state["next_piece"] = random_piece()
    state["status"] = STATE_RUNNING
    return state
