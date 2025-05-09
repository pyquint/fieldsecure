import math
from collections.abc import Iterable
from typing import Tuple

import numpy as np

from app.types import ColumnVector, Matrix, Vector


def is_square(n: int) -> bool:
    return n == math.isqrt(n) ** 2


def is_square_of(k: int, n: int) -> bool:
    return math.sqrt(n) == k


def index_c(c: str) -> int:
    """
    Returns the index of character c from the alphabet.
    """
    offset = 65 if c.isupper() else 97 if c.islower() else 0
    return (ord(c) - offset) % 26


def alpha_i(i: int) -> str:
    """
    Returns the character in the alphabet at index i.
    """
    return chr((i % 26) + 65)


def square_matrix_from_str(string: str) -> np.ndarray[np.int_]:
    length = len(string)
    if not string.isalpha() or not is_square(length):
        print("The key must be letters and n^2 characters long")
    k = math.isqrt(length)
    return np.array(
        [[index_c(c) for c in string[x : x + k]] for x in range(0, len(string), k)]
    )


def column_vector(lst: Iterable) -> ColumnVector:
    """column_vector

    Args:
        lst (Iterable): _description_

    Returns:
        ColumnVector: _description_
    """
    return np.array([[e] for e in lst])


def row_vector(lst: Iterable) -> Vector:
    return np.array([e for e in lst])


def str_from_ndarray(array: np.ndarray) -> str:
    return "".join("".join(alpha_i(i) for i in row) for row in array)


def np_to_latex(matrix: np.ndarray, environment="pmatrix", formatter=str) -> str:
    # https://inakleinbottle.com/posts/formatting-matrices-with-python/
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


def is_invertible(sq_matrix: np.ndarray) -> bool:
    try:
        np.linalg.inv(sq_matrix)
        return True
    except np.linalg.LinAlgError:
        return False


def det(M: np.ndarray) -> int | float:
    """
    Bareiss algorithm to calculate the determinant of a `nxn` square matrix.

    Preserves integer determinant for integer matrices.

    reference: https://stackoverflow.com/a/66192895
    """
    M = M.copy()  # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N - 1):
        if M[i][i] == 0:  # swap with another row having nonzero i's elem
            swapto = next((j for j in range(i + 1, N) if M[j][i] != 0), None)
            if swapto is None:
                return 0  # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i + 1, N):
            for k in range(i + 1, N):
                # assert (M[j][k] * M[i][i] - M[j][i] * M[i][k]) % prev == 0
                M[j][k] = (M[j][k] * M[i][i] - M[j][i] * M[i][k]) / prev
        prev = M[i][i]
    return sign * M[-1][-1]


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)

    reference: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = egcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)


def modinv(a: int, mod: int) -> int:
    """return x such that (x * a) % b == 1

    reference: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    g, x, _ = egcd(a, mod)
    if g != 1:
        raise Exception("gcd(a, b) != 1")
    return x % mod


def split_to_chunks(text: str, chunk_len: int, placeholder: str = "X") -> list[str]:
    chunks = []

    for i in range(0, len(text), chunk_len):
        chunk = text[i : i + chunk_len]

        if len(chunk) < chunk_len:
            missing_chars = chunk_len - len(chunk)
            chunk += placeholder * missing_chars
        chunks.append(chunk)

    return chunks
