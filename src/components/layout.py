from dash import dcc, html
from dash_extensions import EventListener
from game.constants import INITIAL_GAME_STATE, INITIAL_SPEED_MS


def create_layout():
    return html.Div(
        id="app-container",
        children=[

            # ── Stores ───────────────────────────────────────────────────────
            dcc.Store(id="game-state", data=INITIAL_GAME_STATE),

            # ── Ticker ───────────────────────────────────────────────────────
            dcc.Interval(
                id="game-tick",
                interval=INITIAL_SPEED_MS,
                disabled=True,          # enabled only when game is running
                n_intervals=0,
            ),

            # ── Keyboard listener ─────────────────────────────────────────────
            EventListener(
                id="keyboard",
                events=[{"event": "keydown", "props": ["key", "code"]}],
            ),

            # ── Game wrapper ──────────────────────────────────────────────────
            html.Div(
                id="game-wrapper",
                children=[
                    _left_panel(),
                    _board_panel(),
                    _right_panel(),
                ]
            ),
        ]
    )


# ── Private helpers ───────────────────────────────────────────────────────────
# These are only used inside this file, hence the underscore prefix.

def _left_panel():
    return html.Div(
        id="left-panel",
        children=[
            html.H4("HOLD"),
            html.Div(id="held-piece-display"),    # updated by callback
        ]
    )


def _board_panel():
    return html.Div(
        id="board-panel",
        children=[
            html.Div(id="board-container"),       # updated by callback
            html.Div(
                id="game-overlay",                # shown on pause / game over
                children=[],
                style={"display": "none"},
            ),
        ]
    )


def _right_panel():
    return html.Div(
        id="right-panel",
        children=[
            html.H4("NEXT"),
            html.Div(id="next-piece-display"),    # updated by callback

            html.H4("SCORE"),
            html.Div(id="score-display", children="0"),

            html.H4("LEVEL"),
            html.Div(id="level-display", children="1"),

            html.H4("LINES"),
            html.Div(id="lines-display", children="0"),

            html.Button("START",  id="start-btn",  n_clicks=0),
            html.Button("PAUSE",  id="pause-btn",  n_clicks=0),
            html.Button("RESTART",id="restart-btn",n_clicks=0),
        ]
    )
