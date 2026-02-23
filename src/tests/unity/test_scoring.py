from game.tetris_engine import calculate_score

def test_single_line_score():
    assert calculate_score(lines=1, level=1) == 100

def test_tetris_score():
    assert calculate_score(lines=4, level=1) == 800

def test_score_scales_with_level():
    assert calculate_score(lines=1, level=2) == 200

def test_zero_lines_no_score():
    assert calculate_score(lines=0, level=1) == 0