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