from re import I

import sympy as sp
from flask import json, jsonify, render_template, request, session

from app.rsa import bp


@bp.route("/rsa", methods=["GET"])
def rsa():
    return render_template("ciphers/rsa.html")


@bp.route("/api/rsa", methods=["GET", "POST"])
def rsa_api():
    message: str = request.args.get("message", "").strip()
    keys: dict = json.loads(request.args.get("keys"))

    mode: str = request.args.get("mode", "encrypt").strip().lower()

    public_key: list[int, int] = keys["public_key"]
    private_key: list[int, int] = keys["private_key"]

    n, d = public_key
    n, e = private_key

    print(f"\n{message=}")
    print(f"{n=}, {d=}")
    print(f"{n=}, {e=}")
    print(f"{mode=}")

    message_to_ascii_code = [ord(c) for c in message]
    # message_to_ascii_code_str = "".join(ord(c) for c in message_to_ascii_code)
    print(f"{message_to_ascii_code=}")

    if mode == "encrypt":
        encrypted_ascii_codes = [pow(m, e, n) for m in message_to_ascii_code]
    else:
        encrypted_ascii_codes = [pow(m, d, n) for m in message_to_ascii_code]

    print(f"{encrypted_ascii_codes=}")

    output = "".join(chr(c) for c in encrypted_ascii_codes)
    print(f"{output=}")

    response = {
        "message": message,
        "keys": keys,
        "message_to_ascii_code": message_to_ascii_code,
        "encrpted_ascii_codes": encrypted_ascii_codes,
        "output": output,
    }

    print(f"\n{response}\n")

    session["rsa_response"] = response

    return jsonify(response)


@bp.route("/render-subtemplate")
def render_subtemplate():
    response = session.get("rsa_response", {})
    session.pop("rsa_response", None)
    return render_template("learn/_hill-cipher.html", **response)


@bp.route("/rsa_generate_keys", methods=["GET", "POST"])
def rsa_generate_keys():
    body_data = request.get_json()
    print(f"\n{body_data=}\n")

    p: str | None = body_data.get("p")
    q: str | None = body_data.get("q")

    print(f"{p=}, {q=}\n")

    errors: dict = {}

    # ? {"p" : ..., "q" : ...}
    for key, val in body_data.items():
        if val:
            if not val.isdigit():
                errors[key] = {"NaN": f"Value of ${key}$ is not a number."}
            elif not sp.isprime(int(val)):
                errors[key] = {"NonPrime": f"${val}$ is not prime."}

    print(f"ERRORS: {errors}\n")
    if errors:
        return jsonify(errors), 400

    p = int(p) if p else sp.randprime(3, 200)
    q = int(q) if q else sp.randprime(3, 200)

    public_key, private_key = generate_keys(p, q)
    print(f"({public_key=}, {private_key=})\n")

    return jsonify(
        {"p": p, "q": q, "public_key": public_key, "private_key": private_key}
    )


def generate_keys(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Calculates the public and private keys from `p` and `q`.

    Returns a tuple of the public and private keys `(n,e) (n,d)`.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)

    return (n, e), (n, d)
    return (n, e), (n, d)
