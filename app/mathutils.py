import math
import random
from collections.abc import Iterable
from math import gcd

import numpy as np
from sympy import isprime, mod_inverse

from app.types import ColumnVector, Vector


def is_square(n):
    return n == math.isqrt(n) ** 2


def is_square_of(k, n):
    return math.sqrt(n) == k


def index_c(c):
    """
    Returns the index of character c from the alphabet.
    """
    return (ord(c) - 65) % 26


def alpha_i(i):
    """
    Returns the character in the alphabet at index i.
    """
    return chr((i % 26) + 65)


def square_matrix_from_str(string: str):
    l = len(string)
    if not string.isalpha() or not is_square(l):
        print("The key must be letters and n^2 characters long")
    k = math.isqrt(l)
    return np.array(
        [[index_c(c) for c in string[x : x + k]] for x in range(0, len(string), k)]
    )


def column_vector(lst: Iterable) -> ColumnVector:
    return np.array([[e] for e in lst])


def row_vector(lst: str) -> Vector:
    return np.array([e for e in str])


def str_from_ndarray(array: np.ndarray):
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


def generate_prime(bits=8):
    """Generate a random prime number with the given bit length."""
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num


def generate_rsa_keys(bits=8):
    """Generate RSA public and private keys."""
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Choose e (common values: 3, 17, 65537)
    e = 3
    while e < phi_n and gcd(e, phi_n) != 1:
        e += 2  # Ensure e is odd

    d = mod_inverse(e, phi_n)

    return {"public": (e, n), "private": (d, n), "p": p, "q": q, "phi": phi_n}


def encrypt_rsa(plaintext, public_key):
    """Encrypt a plaintext message using RSA."""
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt_rsa(ciphertext, private_key):
    """Decrypt a ciphertext using RSA."""
    d, n = private_key
    plaintext = "".join(chr(pow(char, d, n)) for char in ciphertext)
    return plaintext


def is_invertible(sq_matrix: np.ndarray) -> bool:
    try:
        inv = np.linalg.inv(sq_matrix)
        return True
    except np.linalg.LinAlgError:
        return False
