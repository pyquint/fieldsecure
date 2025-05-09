from math import gcd

import sympy as sp
from flask import json, jsonify, render_template, request

from app.ciphers import bp


@bp.route("/rsa", methods=["GET"])
def rsa_view():
    return render_template("ciphers/rsa.html", cipher_endpoint="rsa")


@bp.route("/rsa/cipher", methods=["GET"])
def rsa_cipher():
    message: str = request.args.get("message", "").strip()
    keys: dict = json.loads(request.args.get("keys"))
    mode: str = request.args.get("mode", "encrypt").strip().lower()
    p = request.args.get("p", type=int)
    q = request.args.get("q", type=int)

    public_key: list[int, int] = keys["public_key"]
    private_key: list[int, int] = keys["private_key"]

    n, e = public_key
    n, d = private_key
    phi = (p - 1) * (q - 1)

    print(f"\n{message=}\n")
    print(f"{keys=}\n")
    print(f"{p=}, {q=}\n")
    print(f"{n=}, {e=}\n")
    print(f"{n=}, {d=}\n")
    print(f"{phi=}")
    print(f"{mode=}\n")

    message_to_ascii_code = [ord(c) for c in message]
    # message_to_ascii_code_str = "".join(ord(c) for c in message_to_ascii_code)
    print(f"{message_to_ascii_code=}")

    if mode == "encrypt":
        print("encrypt")
        print(
            f"{message_to_ascii_code[0]}^{e} mod {n}",
            pow(message_to_ascii_code[0], e, n),
        )
        encrypted_ascii_codes = [pow(m, e, n) for m in message_to_ascii_code]
    else:
        print("decrypt")
        print(
            f"{message_to_ascii_code[0]}^{d} mod {n}={pow(message_to_ascii_code[0], e, n)}"
        )
        encrypted_ascii_codes = [pow(m, d, n) for m in message_to_ascii_code]

    print(f"{encrypted_ascii_codes=}")

    output = "".join(chr(c) for c in encrypted_ascii_codes)
    print(f"{output=}")

    variables = dict(
        message=message,
        p=p,
        q=q,
        n=n,
        e=e,
        d=d,
        phi=phi,
        message_to_ascii_code=message_to_ascii_code,
        encrypted_ascii_codes=encrypted_ascii_codes,
        output=output,
    )

    print(f"\n{variables}\n")

    return render_template("learn/_rsa.html", **variables)


@bp.route("/rsa/generate_keys", methods=["GET"])
def rsa_generate_keys():
    p: str | None = request.args.get("p")
    q: str | None = request.args.get("q")
    e: str | None = request.args.get("e")

    print(f"{p=}, {q=}, {e=}\n")

    errors: dict = {}

    for key, val in request.args.items():
        if val:
            if not val.isdigit():
                errors[key] = f"Value of ${key}$ is not a number."
            elif not sp.isprime(int(val)):
                errors[key] = f"${val}$ is not prime."

    print(f"ERRORS: {errors}\n")

    if errors:
        return jsonify(errors), 400

    p = int(p) if p else sp.randprime(3, 200)
    q = int(q) if q else sp.randprime(3, 200)

    if e:
        try:
            public_key, private_key = generate_keys(p, q, int(e))
        except ValueError as e:
            errors["e"] = {"NonCoprime": "$e$ must be coprime to $\\phi(n)$"}
            return errors, 400
    else:
        public_key, private_key = generate_keys(p, q)

    print(f"({public_key=}, {private_key=})\n")

    return {"p": p, "q": q, "public_key": public_key, "private_key": private_key}


def generate_keys(
    p: int, q: int, e: int = 65537
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Calculates the public and private keys from `p` and `q`.

    If `e` is omitted, the "standard" value is used, which is currently 65537.

    Returns a tuple of the public and private keys `(n,e) (n,d)`.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"{phi=}\n")

    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime to phi(n)")

    d = pow(e, -1, phi)

    return (n, e), (n, d)
