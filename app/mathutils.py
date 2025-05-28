import math
from collections.abc import Iterable
from string import ascii_lowercase
from typing import Tuple

import numpy as np
import sympy as sp
from itsdangerous import exc

from app.types import ColumnVector, Vector


def is_square(n: int) -> bool:
    return n == math.isqrt(n) ** 2


def is_square_of(k: int, n: int) -> bool:
    return math.sqrt(n) == k


def alpha_id(c: str) -> int:
    """
    Returns the index of character c from the English alphabet.
    """
    if not c.isalpha():
        raise ValueError(f"{c} is not a letter in the English alphabet.")
    return ascii_lowercase.index(c.lower())


def id_alpha_upper(i: int) -> str:
    """
    Returns the lowercase character in the alphabet at index i.
    """
    return chr((i % 26) + 65)


def id_alpha_lower(i: int) -> str:
    """
    Returns the lowercase character in the alphabet at index i.
    """
    return chr((i % 26) + 97)


def square_matrix_from_str(string: str) -> np.ndarray[np.int_]:
    length = len(string)
    if not string.isalpha() or not is_square(length):
        print("The key must be letters and n^2 characters long")
    k = math.isqrt(length)
    return np.array(
        [[alpha_id(c) for c in string[x : x + k]] for x in range(0, len(string), k)]
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


def lst_from_ndarray(array: np.ndarray):
    return array.flatten()


def str_from_ndarray(array: np.ndarray) -> str:
    return "".join("".join(id_alpha_upper(i) for i in row) for row in array)


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


def is_invertible(matrix: np.ndarray) -> bool:
    try:
        np.linalg.inv(matrix)
        sp.mod_inverse(det(matrix), 26)
        return True
    except np.linalg.LinAlgError as e:
        print("Error:", e)
        return False
    except ValueError as e:
        print("Error:", e)
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


def generate_unique_primes(
    n: int = 2, minimum: int = 2, maximum: int = 200
) -> set[int]:
    """
    Generate a set of primes.

    :param n: desired number of primes
    :type n: int
    :param minimum: Minimum lookup range, default 2
    :type minimum: int
    :param maximum: Maximum loopup range, default 200
    :type maximum: int
    :return: Unique set of primes
    :rtype: set[int]
    """

    primes = set()

    # ensures the loop runs in a limited number of iterations
    for i in range(maximum - minimum):
        primes.add(sp.randprime(minimum, maximum))
        if len(primes) == n:
            return primes
    else:
        raise Exception("Not enough primes within range.")


def shift_string(s: str, n: int):
    """Shift the characters in the string.

    Args:
        s (str): The string to be shifted.
        n (int): Amount of shift. Positive shifts to right, negative to the left.

    Returns:
        str: Shifted message.
    """
    n = n % len(s)
    return s[-n:] + s[:-n]


def filter_alpha(s: str) -> str:
    """Removes non-alphabet characters from string `s`.

    Args:
        s (str): The string to be filtered.

    Returns:
        str: String `s` but letters only.
    """
    return "".join(c for c in s if c.isalpha())
