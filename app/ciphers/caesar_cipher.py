from string import ascii_uppercase

from flask import Response, jsonify, render_template, request

from app.ciphers import bp
from app.mathutils import shift_string


@bp.route("/caesar-cipher", methods=["GET"])
def caesar_cipher_view():
    return render_template(
        "ciphers/caesar_cipher.html", cipher_endpoint="caesar-cipher"
    )


@bp.route("/caesar-cipher/cipher", methods=["GET"])
def caesar_cipher() -> tuple[Response, int] | str:
    message: str = request.args.get("message")
    shift: int = request.args.get("shift", type=int)

    if not shift:
        return jsonify({"shift": "Shift value is invalid."}), 400

    print(f"\n{message=}\n")
    print(f"{shift=}\n")

    shifted_alphabet = shift_string(ascii_uppercase, shift)

    output = "".join(_caesar_cipher(message, shift))
    print(f"{output=}\n")

    response = dict(
        message=message, shift=shift, shifted_alphabet=shifted_alphabet, output=output
    )
    print(f"{response=}\n")

    return render_template("learn/_caesar_cipher.html", **response)


def _caesar_cipher(message, n):
    for c in message:
        if c.isalpha():
            start = ord("a") if c.islower() else ord("A")
            shifted_char = chr(start + (ord(c) - start + n) % 26)
            yield shifted_char
        else:
            yield c
