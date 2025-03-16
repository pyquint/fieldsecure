from flask import jsonify, render_template, request

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
    return jsonify(response)
