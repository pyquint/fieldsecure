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
def hill_cipher() -> tuple[Response, int] | str:
    original_message: str = request.args.get("message", "").strip()
    key: str = request.args.get("key", "").strip()
    keysize: int = request.args.get("keysize", type=int)
    mode: str = request.args.get("mode", "").strip().lower()

    if mode not in ("encrypt", "decrypt"):
        return jsonify({"mode": 'Mode must be either "encrypt" or "decrypt".'}), 400

    if not key.isalpha():
        return jsonify({"key": "Key must be letters only."}), 400
    elif len(key) != keysize:
        return jsonify({"key": "Non-matching key and key size."}), 400

    keysize: int = len(key)

    message = mu.filter_alpha(original_message)
    chunk_size = isqrt(keysize)

    # split message into k-length chunks
    msg_chunks: list[str] = mu.split_to_chunks(message, chunk_size)
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
        [mu.alpha_id(c) for c in chunk] for chunk in msg_chunks
    ]
    print(f"{msg_num_chunks=}")

    # column vector representation of the chunks, in indices
    msg_chunk_num_vectors: list[ColumnVector[np.int_]] = [
        mu.column_vector(chunk) for chunk in msg_num_chunks
    ]
    print(f"{msg_chunk_num_vectors=}")

    key_matrix: Matrix[np.int_] = mu.square_matrix_from_str(key)
    print(f"{key_matrix=}")

    if not mu.is_invertible(key_matrix):
        # example non-invertible matrix: np.array([[9, 6], [12, 8]])
        return jsonify({"key": "Key matrix is not invertible."}), 400

    # decryption vars
    # use the inverse to decrypt
    det = mu.det(key_matrix) % 26
    print(f"{det=}")

    modinv = sp.mod_inverse(det, 26)
    print(f"{modinv=}")

    adjugate: sp.Matrix = (
        sp.Matrix(key_matrix).adjugate().applyfunc(lambda x: (x + 26) % 26)
    )
    print(f"{adjugate=}")

    inv_key_matrix = modinv * adjugate % 26
    print(f"{inv_key_matrix=}")
    # end decryption vars

    if mode == "encrypt":
        dot_products: list[ColumnVector[np.int_]] = [
            np.dot(key_matrix, vectors) for vectors in msg_chunk_num_vectors
        ]
    else:
        dot_products: list[ColumnVector[np.int_]] = [
            np.dot(inv_key_matrix, vectors) for vectors in msg_chunk_num_vectors
        ]

    print(f"{dot_products=}")

    products_modulos: list[ColumnVector[np.int_]] = [
        product % 26 for product in dot_products
    ]
    print(f"{products_modulos=}")

    output_chunks_int_flat = [
        i for vector in products_modulos for i in mu.lst_from_ndarray(vector)
    ]
    print(f"{output_chunks_int_flat=}")

    output_chunks_int_vectors = [
        mu.column_vector(chunk)
        for chunk in mu.split_to_chunks(output_chunks_int_flat, chunk_size)
    ]
    print(f"{output_chunks_int_vectors=}")

    output_char_list = [
        mu.id_alpha_lower(id) if message[i].islower() else mu.id_alpha_upper(id)
        for i, id in enumerate(output_chunks_int_flat)
    ]
    print(f"{output_char_list=}")

    output_chunk_char_vectors = [
        mu.column_vector(chunk)
        for chunk in mu.split_to_chunks(output_char_list, chunk_size)
    ]
    print(f"{output_chunk_char_vectors=}")

    output = "".join(output_char_list)
    print(f"{output=}\n")

    response = {
        "mode": mode,
        "original_message": original_message,
        "message": message,
        "key": key,
        "k": keysize,
        "key_matrix": mu.np_to_latex(key_matrix),
        "inv_key_matrix": mu.np_to_latex(inv_key_matrix),
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
        "output_chunk_int_vectors": [
            mu.np_to_latex(vector) for vector in output_chunk_char_vectors
        ],
        "output_chunk_char_vectors": [
            mu.np_to_latex(vector) for vector in output_chunk_char_vectors
        ],
        "output_char_list": output_char_list,
        "output": output,
    }

    return render_template("learn/_hill-cipher.html", **response)
