import sympy as sp
from flask import json, jsonify, request

from app.api import bp
from app.ciphers.rsa import generate_keys


@bp.route("/api/rsa", methods=["GET"])
def rsa_api():
    message: str = request.args.get("message", "").strip()
    keys: dict = json.loads(request.args.get("keys"))
    mode: str = request.args.get("mode", "encrypt").strip().lower()

    p = request.args.get("p", type=int)
    q = request.args.get("q", type=int)
    phi: int = (p - 1) * (q - 1)

    public_key: list[int, int] = keys["public_key"]
    private_key: list[int, int] = keys["private_key"]

    n, e = public_key
    n, d = private_key

    message_to_ascii_code = [ord(c) for c in message]

    if mode == "encrypt":
        encrypted_ascii_codes = [pow(m, e, n) for m in message_to_ascii_code]
    else:
        encrypted_ascii_codes = [pow(m, d, n) for m in message_to_ascii_code]

    output = "".join(chr(c) for c in encrypted_ascii_codes)

    return jsonify(
        {
            "message": message,
            "p": p,
            "q": q,
            "n": n,
            "e": e,
            "d": d,
            "phi": phi,
            "message_to_ascii_code": message_to_ascii_code,
            "encrpted_ascii_codes": encrypted_ascii_codes,
            "output": output,
        }
    )


@bp.route("/rsa/generate_keys", methods=["GET"])
def rsa_generate_keys():
    p: str | None = request.args.get("p")
    q: str | None = request.args.get("q")
    e: str | None = request.args.get("e")

    errors: dict = {}

    for key, val in request.args.items():
        if val:
            if not val.isdigit():
                errors[key] = f"Value of ${key}$ is not a number."
            elif not sp.isprime(int(val)):
                errors[key] = f"${val}$ is not prime."

    if errors:
        return jsonify(errors), 400

    p = int(p) if p else sp.randprime(3, 200)
    q = int(q) if q else sp.randprime(3, 200)

    if e:
        try:
            public_key, private_key = generate_keys(p, q, int(e))
        except ValueError:
            errors["e"] = {"NonCoprime": "$e$ must be coprime to $\\phi(n)$"}
            return errors, 400
    else:
        public_key, private_key = generate_keys(p, q)

    return {"p": p, "q": q, "public_key": public_key, "private_key": private_key}
