import dash
from dash import dcc, html
from dash_extensions import EventListener
from game.constants import INITIAL_GAME_STATE, INITIAL_SPEED_MS

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(id="app-container", children=[

    # --- Stores (game memory) ---
    dcc.Store(id="game-state", data=INITIAL_GAME_STATE),
    dcc.Store(id="key-store", data={"key": ""}),

    # --- Game tick (auto-drop pieces) ---
    dcc.Interval(id="game-tick", interval=INITIAL_SPEED_MS, disabled=True),

    # --- Keyboard listener ---
    EventListener(
        id="keyboard",
        events=[{"event": "keydown", "props": ["key", "code"]}],
    ),

    # --- UI ---
    html.Div(id="game-wrapper", children=[
        html.Div(id="side-panel-left", children=[
            html.H4("HOLD"),
            html.Div(id="held-piece-display"),
        ]),
        html.Div(id="board-container", children=[
            html.Div(id="game-board"),   # rendered here
        ]),
        html.Div(id="side-panel-right", children=[
            html.H4("NEXT"),
            html.Div(id="next-piece-display"),
            html.H4("SCORE"),
            html.Div(id="score-display", children="0"),
            html.H4("LEVEL"),
            html.Div(id="level-display", children="1"),
            html.H4("LINES"),
            html.Div(id="lines-display", children="0"),
            html.Button("START", id="start-btn"),
            html.Button("PAUSE", id="pause-btn"),
        ]),
    ]),
])

if __name__ == "__main__":
    app.run(debug=True)
