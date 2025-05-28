from math import ceil

from flask import Response, jsonify, render_template, request

from app.ciphers import bp
from app.mathutils import alpha_id, id_alpha_upper


@bp.route("/vigenere-cipher", methods=["GET"])
def vigenere_cipher_view():
    return render_template(
        "ciphers/vigenere_cipher.html", cipher_endpoint="vigenere-cipher"
    )


@bp.route("/vigenere-cipher/cipher", methods=["GET"])
def vigenere_cipher() -> tuple[Response, int] | str:
    message: str = request.args.get("message")
    original_key: str = request.args.get("key")
    mode: str = request.args.get("mode")

    if not (original_key or original_key.isalpha()):
        return jsonify({"key": "Key value is invalid."}), 400

    print(f"\n{mode=}\n")
    print(f"{message=}\n")
    print(f"{original_key=}\n")

    cleaned_message = "".join(c for c in message.upper() if c.isalpha())
    message_to_int: list[int] = [alpha_id(c) for c in cleaned_message]
    print(f"{cleaned_message=}\n")
    print(f"{message_to_int=}\n")

    key: str = extend_key(message, original_key.upper())
    key_to_int = [alpha_id(k) for k in key]
    print(f"{key=}\n")
    print(f"{key_to_int=}\n")

    if mode == "encrypt":
        sum_plaintext_key = [(p + k) % 26 for p, k in zip(message_to_int, key_to_int)]
    elif mode == "decrypt":
        sum_plaintext_key = [(p - k) % 26 for p, k in zip(message_to_int, key_to_int)]
    else:
        return jsonify({"message": "`mode` is invalid."}), 400

    print(f"{sum_plaintext_key=}\n")

    output = "".join(id_alpha_upper(c) for c in sum_plaintext_key)
    print(f"{output=}\n")

    response = dict(
        message=message,
        cleaned_message=cleaned_message,
        original_key=original_key,
        key=key,
        message_to_int=message_to_int,
        key_to_int=key_to_int,
        sum_plaintext_key=sum_plaintext_key,
        output=output,
    )
    print(f"{response=}\n")

    return render_template("learn/_vigenere_cipher.html", **response)


def extend_key(message, key):
    msg_len = len(message)
    key_len = len(key)
    extend_by = ceil(msg_len / key_len)

    return (key + (key * extend_by))[0:msg_len]
