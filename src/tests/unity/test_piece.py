import numpy as np
from game.pieces import TETROMINOES
from game.tetris_engine import get_piece_matrix

def test_all_pieces_defined():
    for name in ["I", "O", "T", "S", "Z", "J", "L"]:
        assert name in TETROMINOES

def test_o_piece_rotation_unchanged():
    original = TETROMINOES["O"].copy()
    rotated = get_piece_matrix("O", rotation=0)   # rotation=0 means no rotation
    assert np.array_equal(original, rotated)

def test_i_piece_is_4x4():
    assert TETROMINOES["I"].shape == (4, 4)

def test_rotation_returns_numpy_array():
    result = get_piece_matrix("T", rotation=1)
    assert isinstance(result, np.ndarray)