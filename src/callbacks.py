from dash import Input, Output, State, set_props
from game.tetris_engine import handle_key_input, apply_game_tick, start_game, calculate_speed
from game.constants import STATE_RUNNING, STATE_PAUSED, INITIAL_SPEED_MS
from components.board import render_board, render_mini_board


def register_callbacks(app):

    # ── Start / Restart ───────────────────────────────────────────────────────

    @app.callback(
        Output("game-state", "data"),
        Input("start-btn", "n_clicks"),
        Input("restart-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_start_restart(start_clicks, restart_clicks):
        state = start_game()
        #enable dcc.interval
        set_props("game-tick", {"disabled": False})
        return state


    # ── Pause button ──────────────────────────────────────────────────────────

    @app.callback(
        Output("game-state", "data"),
        Output("game-tick", "disabled"),
        Input("pause-btn", "n_clicks"),
        State("game-state", "data"),
        prevent_initial_call=True,
    )
    def on_pause(n_clicks, state):
        if not state:
            return state, True
        if state["status"] == STATE_RUNNING:
            state["status"] = STATE_PAUSED
            return state, True
        elif state["status"] == STATE_PAUSED:
            state["status"] = STATE_RUNNING
            return state, False
        return state, True


    # ── Keyboard ──────────────────────────────────────────────────────────────

    @app.callback(
        Output("game-state", "data"),
        Input("keyboard", "event"),
        State("game-state", "data"),
        prevent_initial_call=True,
    )
    def on_key(event, state):
        if event and state:
            return handle_key_input(state, event["key"])
        return state


    # ── Game tick ─────────────────────────────────────────────────────────────

    @app.callback(
        Output("game-state", "data"),
        Output("game-tick", "interval"),
        Input("game-tick", "n_intervals"),
        State("game-state", "data"),
        prevent_initial_call=True,
    )
    def on_tick(n_intervals, state):
        if not state:
            return state, INITIAL_SPEED_MS
        state = apply_game_tick(state)
        speed = calculate_speed(state["level"])
        return state, speed


    # ── Render board ──────────────────────────────────────────────────────────

    @app.callback(
        Output("board-container", "children"),
        Input("game-state", "data"),
    )
    def render(state):
        if not state or state["status"] == "idle":
            return []
        return render_board(state)


    # ── Render side panels ────────────────────────────────────────────────────

    @app.callback(
        Output("next-piece-display", "children"),
        Output("held-piece-display", "children"),
        Output("score-display", "children"),
        Output("level-display", "children"),
        Output("lines-display", "children"),
        Input("game-state", "data"),
    )
    def update_ui(state):
        if not state:
            return [], [], "0", "1", "0"
        return (
            render_mini_board(state["next_piece"]),
            render_mini_board(state.get("held_piece")),
            str(state["score"]),
            str(state["level"]),
            str(state["lines_cleared"]),
        )
