from flask import jsonify, render_template, request

from app.rsa import bp


@bp.route("/rsa", methods=["GET"])
def rsa():
    # holy shit this works
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        text = request.args.get("text", "")
        response = {
            "output": f"(RSA:{text})",
            "steps": render_template("ciphers/learn/rsa.html", text=text),
        }
        print(f"\n{response}\n")
        return jsonify(response)
    else:
        return render_template("ciphers/rsa.html")
