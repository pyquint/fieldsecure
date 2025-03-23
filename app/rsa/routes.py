import sympy
from flask import jsonify, render_template, request, session

from app.rsa import bp


@bp.route("/rsa", methods=["GET"])
def rsa():
    return render_template("ciphers/rsa.html")


@bp.route("/api/rsa", methods=["POST"])
def rsa_api():
    text = request.args.get("text", "")
    response = {
        "output": f"(RSA:{text})",
        "steps": render_template("learn/_rsa.html", text=text),
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

    errors = {}

    for key, val in body_data.items():
        if val:
            if not val.isdigit():
                errors[key] = {"NaN": f"Value of ${key}$ is not a number."}
            elif not sympy.isprime(int(val)):
                errors[key] = {"NonPrime": f"${val}$ is not prime."}

    print(f"\nERRORS: {errors}\n")
    if errors:
        return jsonify(errors), 400

    p = int(p) if p else sympy.randprime(3, 200)
    q = int(q) if q else sympy.randprime(3, 200)

    public_key, private_key = generate_keys(p, q) if p and q else generate_keys()
    print(f"({public_key=}, {private_key=})\n")

    return jsonify(
        {"p": p, "q": q, "public_key": public_key, "private_key": private_key}
    )


def generate_keys(p: int, q: int):
    """
    Calculates the public and private keys from `p` and `q`.

    Returns a tuple of the public and private keys `(n,e) (n,d)`.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)

    return (n, e), (n, d)
