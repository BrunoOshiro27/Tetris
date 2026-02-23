import numpy as np

# All 7 tetrominoes in their default rotation
TETROMINOES = {
    "I": np.array([[0,0,0,0],
                   [1,1,1,1],
                   [0,0,0,0],
                   [0,0,0,0]]),

    "O": np.array([[1,1],
                   [1,1]]),

    "T": np.array([[0,1,0],
                   [1,1,1],
                   [0,0,0]]),

    "S": np.array([[0,1,1],
                   [1,1,0],
                   [0,0,0]]),

    "Z": np.array([[1,1,0],
                   [0,1,1],
                   [0,0,0]]),

    "J": np.array([[1,0,0],
                   [1,1,1],
                   [0,0,0]]),

    "L": np.array([[0,0,1],
                   [1,1,1],
                   [0,0,0]]),
}
