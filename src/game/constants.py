# Board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 35          # pixels per cell

# Game timing
INITIAL_SPEED_MS = 500  # how fast pieces fall (milliseconds)
SPEED_INCREMENT = 50    # speed increase per level
MIN_SPEED_MS = 100      # max speed cap

# Colors (one per tetromino type + empty)
COLORS = {
    0: "#1a1a2e",        # empty cell
    1: "#00f5ff",        # I - cyan
    2: "#ffd700",        # O - yellow
    3: "#a855f7",        # T - purple
    4: "#22c55e",        # S - green
    5: "#ef4444",        # Z - red
    6: "#3b82f6",        # J - blue
    7: "#f97316",        # L - orange
    "ghost": "#444466",  # ghost piece
    "grid": "#2a2a4a",   # grid lines
}

# Scoring system
SCORE_TABLE = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,   # Tetris!
}

# Game states
STATE_IDLE = "idle"
STATE_RUNNING = "running"
STATE_PAUSED = "paused"
STATE_OVER = "gameover"

# Initial state 
INITIAL_GAME_STATE = {
    "board": [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],  # uses the constants above
    "current_piece": {
        "shape": "T",
        "rotation": 0,
        "x": 3,
        "y": 0,
        "color_id": 3
    },
    "next_piece": "I",
    "held_piece": None,
    "can_hold": True,
    "score": 0,
    "level": 1,
    "lines_cleared": 0,
    "status": STATE_IDLE,
    "tick": 0
}

# Key bindings
KEY_ACTIONS = {
    "ArrowLeft":  "move_left",
    "ArrowRight": "move_right",
    "ArrowDown":  "soft_drop",
    "ArrowUp":    "rotate_clockwise",
    "z":          "rotate_counter",
    " ":          "hard_drop",
    "c":          "hold_piece",
    "p":          "pause",
    "Escape":     "pause",
}

PIECE_IDS = {
    "I": 1,
    "O": 2,
    "T": 3,
    "S": 4,
    "Z": 5,
    "J": 6,
    "L": 7,
}