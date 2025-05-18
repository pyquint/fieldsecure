from string import ascii_uppercase

from flask import Response, jsonify, render_template, request

from app.ciphers import bp
from app.mathutils import shift_right


@bp.route("/caesar-cipher", methods=["GET"])
def caesar_cipher_view():
    return render_template(
        "ciphers/caesar_cipher.html", cipher_endpoint="caesar-cipher"
    )


@bp.route("/caesar-cipher/cipher", methods=["GET"])
def caesar_cipher() -> Response:
    message: str = request.args.get("message")
    shift: int = request.args.get("shift", type=int)

    if not shift:
        return jsonify({"shift": "Shift value is invalid."}), 400

    print(f"\n{message=}\n")
    print(f"{shift=}\n")

    shifted_alphabet = shift_right(ascii_uppercase, shift)

    output = "".join(shift_right(message, shift))
    print(f"{output=}\n")

    response = dict(
        message=message, shift=shift, shifted_alphabet=shifted_alphabet, output=output
    )
    print(f"{response=}\n")

    return render_template("learn/_caesar_cipher.html", **response)
