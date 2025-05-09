from string import ascii_lowercase, ascii_uppercase
from typing import Generator

from flask import Response, jsonify, render_template, request

from app.ciphers import bp
from app.mathutils import index_c


@bp.route("/atbash-cipher", methods=["GET"])
def atbash_cipher_view():
    return render_template("ciphers/atbash_cipher.html", cipher_endpoint="atbash-cipher")


@bp.route("/atbash-cipher/cipher", methods=["GET"])
def atbash_cipher() -> Response:
    message: str = request.args.get("message")
    print(f"\n{message=}\n")

    output = "".join(cipher_atbash(message))
    print(f"{output=}\n")

    response = dict(message=message, output=output)
    print(f"{response=}\n")

    return render_template("learn/_atbash_cipher.html", **response)


def cipher_atbash(message: str) -> Generator[str]:
    reversed_lowercase = ascii_lowercase[::-1]
    reversed_uppercase = ascii_uppercase[::-1]

    for c in message:
        reversed = reversed_lowercase if c.islower() else reversed_uppercase
        if c.isalpha() and not c.isspace():
            yield reversed[index_c(c)]
        else:
            yield c
