import math

import numpy as np


def is_square(n):
    return n == math.isqrt(n) ** 2


def is_square_of(k, n):
    return math.sqrt(n) == k


def index_c(c):
    return (ord(c) - 65) % 26


def alpha_i(i):
    return chr((i % 26) + 65)


def square_matrix_from_str(string: str):
    l = len(string)
    if not string.isalpha() or not is_square(l):
        print("The key must be letters and n^2 characters long")
    k = math.isqrt(l)
    return np.array(
        [[index_c(c) for c in string[x : x + k]] for x in range(0, len(string), k)]
    )


def str_from_ndarray(array):
    return "".join("".join(alpha_i(i) for i in row) for row in array)


# https://inakleinbottle.com/posts/formatting-matrices-with-python/
def np_to_latex(matrix: np.ndarray, environment="bmatrix", formatter=str) -> str:
    """Format a matrix using LaTeX syntax"""

    if not isinstance(matrix, np.ndarray):
        try:
            matrix = np.array(matrix)
        except Exception:
            raise TypeError("Could not convert to Numpy array")

    if len(shape := matrix.shape) == 1:
        matrix = matrix.reshape(1, shape[0])
    elif len(shape) > 2:
        raise ValueError("Array must be 2 dimensional")

    body_lines = [" & ".join(map(formatter, row)) for row in matrix]

    body = "\\\\\n".join(body_lines)
    return f"\\begin{{{environment}}}\n{body}\n\\end{{{environment}}}"


def inversible_key(k):
    pass
