import re

import numpy as np
from flask import jsonify, render_template, request, session

from app.hill_cipher import bp
from app.mathutils import (
    column_vector,
    index_c,
    is_invertible,
    np_to_latex,
    square_matrix_from_str,
    str_from_ndarray,
)
from app.types import ColumnVector, Matrix


@bp.route("/hill-cipher", methods=["GET", "POST"])
def hill_cipher():
    return render_template("ciphers/hill-cipher.html")


@bp.route("/api/hill-cipher", methods=["GET", "POST"])
def hill_cipher_api():
    message: str = request.args.get("message", "").strip()
    key: str = request.args.get("key", "").strip()
    # k is either 2 or 3
    k = request.args.get("k", type=int)

    # remove special characters
    message = re.sub("[^a-zA-Z0-9 \n.]", "", message)

    # split message into k-length chunks
    msg_chunks: list[str] = split_to_chunks(message, k)
    message = "".join(msg_chunks)

    print(f"{message=}")
    print(f"{key=}")
    print(f"{k=}")

    print(f"{msg_chunks=}")

    # column vector representation of the chunks, in letters
    msg_chunk_char_vectors: list[ColumnVector[np.str_]] = [
        column_vector(chunk) for chunk in msg_chunks
    ]
    print(f"{msg_chunk_char_vectors=}")

    # convert the letters in the chunks into alphabet indices
    msg_num_chunks: list[list[int]] = [
        [index_c(c) for c in chunk] for chunk in msg_chunks
    ]
    print(f"{msg_num_chunks=}")

    # column vector representation of the chunks, in indices
    msg_chunk_num_vectors: list[ColumnVector[np.int_]] = [
        column_vector(chunk) for chunk in msg_num_chunks
    ]
    print(f"{msg_chunk_num_vectors=}")

    key_matrix: Matrix[np.int_] = square_matrix_from_str(key)
    print(f"{key_matrix=}")

    # example non-invertible matrix: np.array([[9, 6], [12, 8]])
    print("Is the key matrix invertible?", is_invertible(key_matrix))
    if not is_invertible(key_matrix):
        return jsonify(message="Key matrix is not invertible."), 500

    dot_products: list[ColumnVector[np.int_]] = [
        np.dot(key_matrix, vectors) for vectors in msg_chunk_num_vectors
    ]
    print(f"{dot_products=}")

    products_modulos: list[ColumnVector[np.int_]] = [
        product % 26 for product in dot_products
    ]
    print(f"{products_modulos=}")

    output_chunks = [str_from_ndarray(vector) for vector in products_modulos]
    print(f"{output_chunks=}")

    output_chunk_char_vectors = [column_vector(chunk) for chunk in output_chunks]

    output = "".join(output_chunks)
    print(f"{output=}")

    response = {
        "parameters": {"message": message, "key": key, "k": k},
        "key_matrix": np_to_latex(key_matrix),
        "message_chunks": msg_chunks,
        "message_chunk_vectors": [
            np_to_latex(vector) for vector in msg_chunk_char_vectors
        ],
        "message_chunk_num_vectors": [
            np_to_latex(vector) for vector in msg_chunk_num_vectors
        ],
        "key_vector_dot_products": [
            np_to_latex(dot_product) for dot_product in dot_products
        ],
        "product_modulos": [np_to_latex(modulo) for modulo in products_modulos],
        "output_chunk_char_vectors": [
            np_to_latex(vector) for vector in output_chunk_char_vectors
        ],
        "output_char_chunks": output_chunks,
        "output": output,
    }

    session["hill_cipher_response"] = response

    return jsonify(response)


@bp.route("/render-subtemplate")
def render_subtemplate():
    response = session.get("hill_cipher_response", {})
    session.pop("hill_cipher_response", None)
    return render_template("learn/_hill-cipher.html", **response)


@bp.app_template_filter()
def nptl(nparray: np.ndarray):
    return np_to_latex(nparray)


@bp.app_template_filter()
def join(latexes: list[str], sep=","):
    return sep.join(latexes)


def split_to_chunks(text: str, chunk_len: int, placeholder: str = "X") -> list[str]:
    chunks = []

    for i in range(0, len(text), chunk_len):
        chunk = text[i : i + chunk_len]

        if len(chunk) < chunk_len:
            missing_chars = chunk_len - len(chunk)
            chunk += placeholder * missing_chars
        chunks.append(chunk)

    return chunks
