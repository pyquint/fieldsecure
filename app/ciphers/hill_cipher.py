from math import isqrt

import numpy as np
import sympy as sp
from flask import Response, jsonify, render_template, request

import app.mathutils as mu
from app.ciphers import bp
from app.types import ColumnVector, Matrix


@bp.route("/hill-cipher", methods=["GET"])
def hill_cipher_view():
    return render_template("ciphers/hill-cipher.html", cipher_endpoint="hill-cipher")


@bp.route("/hill-cipher/cipher", methods=["GET"])
def hill_cipher() -> Response:
    message: str = request.args.get("message", "").strip().upper()
    key: str = request.args.get("key", "").strip().upper()
    keysize: int = request.args.get("keysize", type=int)
    mode: str = request.args.get("mode", "").strip().lower()

    if mode not in ("encrypt", "decrypt"):
        return jsonify({"mode": 'Mode must be either "encrypt" or "decrypt".'}), 400

    if not key.isalpha():
        return jsonify({"key": "Key must be letters only."}), 400
    elif len(key) != keysize:
        return jsonify({"key": "Non-matching key and key size."}), 400

    keysize: int = len(key)

    # remove special characters
    # message = re.sub(r"[^a-zA-Z0-9 \n.]", "", message)
    # print(f"only letters: {message=}")

    # split message into k-length chunks
    msg_chunks: list[str] = mu.split_to_chunks(message, isqrt(keysize))
    message = "".join(msg_chunks)

    print(f"\n{message=}")
    print(f"{key=}")
    print(f"{mode=}")
    print(f"{keysize=}")

    print(f"{msg_chunks=}")

    # column vector representation of the chunks, in letters
    msg_chunk_char_vectors: list[ColumnVector[np.str_]] = [
        mu.column_vector(chunk) for chunk in msg_chunks
    ]
    print(f"{msg_chunk_char_vectors=}")

    # convert the letters in the chunks into alphabet indices
    msg_num_chunks: list[list[int]] = [
        [mu.index_c(c) for c in chunk] for chunk in msg_chunks
    ]
    print(f"{msg_num_chunks=}")

    # column vector representation of the chunks, in indices
    msg_chunk_num_vectors: list[ColumnVector[np.int_]] = [
        mu.column_vector(chunk) for chunk in msg_num_chunks
    ]
    print(f"{msg_chunk_num_vectors=}")

    key_matrix: Matrix[np.int_] = mu.square_matrix_from_str(key)
    print(f"{key_matrix=}")

    if mode == "decrypt":
        # use the inverse to decrypt
        det = mu.det(key_matrix) % 26
        print(f"{det=}")

        modinv = sp.mod_inverse(det, 26)
        print(f"{modinv=}")

        adjugate: sp.Matrix = (
            sp.Matrix(key_matrix).adjugate().applyfunc(lambda x: (x + 26) % 26)
        )
        print(f"{adjugate=}")

        key_matrix = modinv * adjugate % 26
        print(f"inverse_key_matrix={key_matrix}")

    elif not mu.is_invertible(key_matrix):
        # example non-invertible matrix: np.array([[9, 6], [12, 8]])
        return jsonify({"key": "Key matrix is not invertible."}), 400

    dot_products: list[ColumnVector[np.int_]] = [
        np.dot(key_matrix, vectors) for vectors in msg_chunk_num_vectors
    ]
    print(f"{dot_products=}")

    products_modulos: list[ColumnVector[np.int_]] = [
        product % 26 for product in dot_products
    ]
    print(f"{products_modulos=}")

    output_chunks = [mu.str_from_ndarray(vector) for vector in products_modulos]
    print(f"{output_chunks=}")

    output_chunk_char_vectors = [mu.column_vector(chunk) for chunk in output_chunks]

    output = "".join(output_chunks)
    print(f"{output=}\n")

    response = {
        "parameters": {"message": message, "key": key, "k": keysize},
        "key_matrix": mu.np_to_latex(key_matrix),
        "message_chunks": msg_chunks,
        "message_chunk_vectors": [
            mu.np_to_latex(vector) for vector in msg_chunk_char_vectors
        ],
        "message_chunk_num_vectors": [
            mu.np_to_latex(vector) for vector in msg_chunk_num_vectors
        ],
        "key_vector_dot_products": [
            mu.np_to_latex(dot_product) for dot_product in dot_products
        ],
        "product_modulos": [mu.np_to_latex(modulo) for modulo in products_modulos],
        "output_chunk_char_vectors": [
            mu.np_to_latex(vector) for vector in output_chunk_char_vectors
        ],
        "output_char_chunks": output_chunks,
        "output": output,
    }

    return render_template("learn/_hill-cipher.html", **response)
