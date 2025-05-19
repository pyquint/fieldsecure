from string import ascii_lowercase, ascii_uppercase
from typing import Generator

from flask import render_template, request

from app.ciphers import bp
from app.mathutils import alpha_id


@bp.route("/atbash-cipher", methods=["GET"])
def atbash_cipher_view():
    return render_template(
        "ciphers/atbash_cipher.html", cipher_endpoint="atbash-cipher"
    )


@bp.route("/atbash-cipher/cipher", methods=["GET"])
def atbash_cipher() -> str:
    message: str = request.args.get("message")
    print(f"\n{message=}\n")

    output = "".join(cipher_atbash(message))
    print(f"{output=}\n")

    response = dict(message=message, output=output)
    print(f"{response=}\n")

    return render_template("learn/_atbash_cipher.html", **response)


def cipher_atbash(message: str) -> Generator[str]:
    for c in message:
        if c.isalpha():
            alphabet = ascii_lowercase if c.islower() else ascii_uppercase
            yield alphabet[(25 - alpha_id(c)) % 26]
        else:
            yield c
