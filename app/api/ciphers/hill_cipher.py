from math import isqrt

import numpy as np
import sympy as sp
from flask import jsonify, request
from sympy.abc import mu

from app.api import bp
from app.mathutils import split_to_chunks
from app.types import ColumnVector, Matrix


@bp.route("/api/hill-cipher", methods=["GET"])
def hill_cipher_api():
    message: str = request.args.get("message", "").strip().upper()
    key: str = request.args.get("key", "").strip().upper()
    keysize: int = request.args.get("keysize", type=int)
    mode: str = request.args.get("mode", "").strip().lower()

    if not key.isalpha():
        return jsonify(message="Key must be letters only."), 400
    elif len(key) != keysize:
        return jsonify(message="Non-matching key and key size."), 400

    keysize: int = len(key)

    # remove special characters
    # message = re.sub(r"[^a-zA-Z0-9 \n.]", "", message)

    # split message into k-length chunks
    msg_chunks: list[str] = split_to_chunks(message, isqrt(keysize))
    message = "".join(msg_chunks)

    # column vector representation of the chunks, in letters
    msg_chunk_char_vectors: list[ColumnVector[np.str_]] = [
        mu.column_vector(chunk) for chunk in msg_chunks
    ]

    # convert the letters in the chunks into alphabet indices
    msg_num_chunks: list[list[int]] = [
        [mu.index_c(c) for c in chunk] for chunk in msg_chunks
    ]

    # column vector representation of the chunks, in indices
    msg_chunk_num_vectors: list[ColumnVector[np.int_]] = [
        mu.column_vector(chunk) for chunk in msg_num_chunks
    ]

    key_matrix: Matrix[np.int_] = mu.square_matrix_from_str(key)

    if mode == "decrypt":
        # use the inverse to decrypt
        det = mu.det(key_matrix) % 26
        modinv = sp.mod_inverse(det, 26)
        adjugate: sp.Matrix = (
            sp.Matrix(key_matrix).adjugate().applyfunc(lambda x: (x + 26) % 26)
        )
        key_matrix = modinv * adjugate % 26
    elif not mu.is_invertible(key_matrix):
        # example of non-invertible matrix: np.array([[9, 6], [12, 8]]) (JGMI)
        # also, repeating characters as keys are often non-invertible (SASA, FHFH)
        return jsonify(message="Key matrix is not invertible."), 400

    dot_products: list[ColumnVector[np.int_]] = [
        np.dot(key_matrix, vectors) for vectors in msg_chunk_num_vectors
    ]
    products_modulos: list[ColumnVector[np.int_]] = [
        product % 26 for product in dot_products
    ]
    output_chunks = [mu.str_from_ndarray(vector) for vector in products_modulos]
    output_chunk_char_vectors = [mu.column_vector(chunk) for chunk in output_chunks]
    output = "".join(output_chunks)

    response = {
        "parameters": {"message": message, "key": key, "k": keysize},
        "key_matrix": key_matrix,
        "message_chunks": msg_chunks,
        "message_chunk_vectors": msg_chunk_char_vectors,
        "message_chunk_num_vectors": msg_chunk_num_vectors,
        "key_vector_dot_products": dot_products,
        "product_modulos": products_modulos,
        "output_chunk_char_vectors": output_chunk_char_vectors,
        "output_char_chunks": output_chunks,
        "output": output,
    }

    return jsonify(response)
