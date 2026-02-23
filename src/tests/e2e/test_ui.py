import pytest
from dash.testing.application_runners import import_app

pytestmark = pytest.mark.e2e   # marks every test in this file

# ── Fixture ───────────────────────────────────────────────────────────────────

@pytest.fixture
def tetris_app(dash_duo):
    """Starts the Dash app in a real browser before each test."""
    app = import_app("app")
    dash_duo.start_server(app)
    return dash_duo


# ── Layout tests ──────────────────────────────────────────────────────────────

def test_board_renders_on_load(tetris_app):
    """Board container should be visible on page load."""
    tetris_app.wait_for_element("#board-container")


def test_score_starts_at_zero(tetris_app):
    tetris_app.wait_for_text_to_equal("#score-display", "0")


def test_level_starts_at_one(tetris_app):
    tetris_app.wait_for_text_to_equal("#level-display", "1")


def test_lines_starts_at_zero(tetris_app):
    tetris_app.wait_for_text_to_equal("#lines-display", "0")


def test_start_button_exists(tetris_app):
    tetris_app.wait_for_element("#start-btn")


def test_pause_button_exists(tetris_app):
    tetris_app.wait_for_element("#pause-btn")


def test_hold_panel_exists(tetris_app):
    tetris_app.wait_for_element("#held-piece-display")


def test_next_panel_exists(tetris_app):
    tetris_app.wait_for_element("#next-piece-display")


# ── Start game tests ──────────────────────────────────────────────────────────

def test_start_button_click_renders_board(tetris_app):
    """Clicking START should populate the board with cells."""
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")


def test_start_button_shows_next_piece(tetris_app):
    """Next piece preview should be populated after game starts."""
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element("#next-piece-display .cell")


def test_score_still_zero_after_start(tetris_app):
    """Score should still be 0 right after starting — no lines cleared yet."""
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_text_to_equal("#score-display", "0")


# ── Keyboard tests ────────────────────────────────────────────────────────────

def test_left_arrow_does_not_crash(tetris_app):
    """Pressing left arrow while game is running should not throw an error."""
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.driver.find_element("tag name", "body").send_keys("\ue012")  # ArrowLeft


def test_right_arrow_does_not_crash(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.driver.find_element("tag name", "body").send_keys("\ue014")  # ArrowRight


def test_down_arrow_does_not_crash(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.driver.find_element("tag name", "body").send_keys("\ue015")  # ArrowDown


def test_space_hard_drop_does_not_crash(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.driver.find_element("tag name", "body").send_keys(" ")


# ── Pause tests ───────────────────────────────────────────────────────────────

def test_pause_button_click_does_not_crash(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.find_element("#pause-btn").click()


def test_pause_key_does_not_crash(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.driver.find_element("tag name", "body").send_keys("p")


# ── Restart tests ─────────────────────────────────────────────────────────────

def test_restart_resets_score(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.find_element("#restart-btn").click()
    tetris_app.wait_for_text_to_equal("#score-display", "0")


def test_restart_resets_level(tetris_app):
    tetris_app.find_element("#start-btn").click()
    tetris_app.wait_for_element(".cell")
    tetris_app.find_element("#restart-btn").click()
    tetris_app.wait_for_text_to_equal("#level-display", "1")
