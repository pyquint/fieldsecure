import numpy as np
from flask import render_template, request

from app.hill_cipher import bp
from app.mathutils import index_c, np_to_latex, square_matrix_from_str, str_from_ndarray


@bp.route("/hill-cipher", methods=["GET", "POST"])
def hill_cipher():
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        message = request.args.get("message", "")
        key = request.args.get("key", "")

        print(f"{message=}")
        print(f"{key=}")

        msg_char_nums = [index_c(c) for c in message.upper()]

        msg_vector = np.array([[c] for c in msg_char_nums])
        print(f"{msg_vector=}")

        key_matrix = square_matrix_from_str(key)
        print(f"{key_matrix=}")

        dot_product = np.dot(key_matrix, msg_vector)
        print(f"{dot_product=}")

        prod_mod = dot_product % 26
        print(f"{prod_mod=}")

        output = str_from_ndarray(prod_mod)
        print(f"{output=}")

        response = {
            "message": message,
            "message_char_nums": msg_char_nums,
            "key": key,
            "message_vector": np_to_latex(msg_vector),
            "key_matrix": np_to_latex(key_matrix),
            "dot_product": np_to_latex(dot_product),
            "product_mod26": np_to_latex(prod_mod),
            "output": output,
        }

        print()
        for key, val in response.items():
            print(f"{key} : {val}\n")
        print()

        return {
            "output": output,
            "template": render_template(
                "ciphers/learn/hill-cipher.html", hill_cipher=response
            ),
        }

    else:
        return render_template("ciphers/hill-cipher.html")
