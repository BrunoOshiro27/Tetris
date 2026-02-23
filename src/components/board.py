from dash import html
from game.constants import COLORS, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE
from game.tetris_engine import get_piece_matrix, get_ghost_position


def render_cell(color_id, is_ghost=False):
    """Returns a single colored cell div."""
    color = COLORS.get("ghost") if is_ghost else COLORS.get(color_id, COLORS[0])
    return html.Div(style={
        "width":           f"{CELL_SIZE}px",
        "height":          f"{CELL_SIZE}px",
        "backgroundColor": color,
        "border":          f"1px solid {COLORS['grid']}",
        "display":         "inline-block",
        "boxSizing":       "border-box",
    })


def render_board(state):
    """
    Renders the full 10x8 game board as a grid of divs.
    """
    import copy
    board = copy.deepcopy(state["board"])
    cp    = state["current_piece"]

    # ── Overlay current piece ─────────────────────────────────────────────────
    piece_cells = set()
    piece_matrix = get_piece_matrix(cp["shape"], cp["rotation"])

    for row_i, row in enumerate(piece_matrix):
        for col_i, cell in enumerate(row):
            if cell:
                px = cp["x"] + col_i
                py = cp["y"] + row_i
                if 0 <= px < BOARD_WIDTH and 0 <= py < BOARD_HEIGHT:
                    piece_cells.add((py, px))
                    board[py][px] = cp["color_id"]

    # ── Build rows of divs ────────────────────────────────────────────────────
    rows = []
    for row_i in range(BOARD_HEIGHT):
        cells = []
        for col_i in range(BOARD_WIDTH):
            cells.append(render_cell(board[row_i][col_i]))
        rows.append(html.Div(children=cells, style={"display": "block", "lineHeight": "0"}))

    return html.Div(
        id="game-board",
        children=rows,
        style={
            "width":   f"{BOARD_WIDTH * CELL_SIZE}px",
            "height":  f"{BOARD_HEIGHT * CELL_SIZE}px",
        }
    )


def render_mini_board(shape, label=""):
    """
    Renders a small 4x4 preview grid for NEXT and HOLD panels.
    Pass shape=None to render an empty panel.
    """
    from game.pieces import TETROMINOES
    from game.constants import PIECE_IDS

    MINI_SIZE = 25
    grid = [[0] * 4 for _ in range(4)]

    if shape:
        matrix = TETROMINOES[shape]
        color_id = PIECE_IDS[shape]
        # center the piece in the 4x4 grid
        offset_r = (4 - len(matrix)) // 2
        offset_c = (4 - len(matrix[0])) // 2
        for r, row in enumerate(matrix):
            for c, cell in enumerate(row):
                if cell:
                    grid[r + offset_r][c + offset_c] = color_id

    rows = []
    for row in grid:
        cells = [
            html.Div(style={
                "width":           f"{MINI_SIZE}px",
                "height":          f"{MINI_SIZE}px",
                "backgroundColor": COLORS.get(cell, COLORS[0]),
                "border":          f"1px solid {COLORS['grid']}",
                "display":         "inline-block",
                "boxSizing":       "border-box",
            })
            for cell in row
        ]
        rows.append(html.Div(children=cells, style={"display": "block", "lineHeight": "0"}))

    return html.Div(children=[
        html.Div(label, style={"color": "#aaa", "fontSize": "12px", "marginBottom": "4px"}),
        html.Div(children=rows, style={"border": "2px solid #333"}),
    ])
