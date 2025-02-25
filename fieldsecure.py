import rsa
from flask import Flask, jsonify, render_template, request
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {"fieldsecure": ("static/sass", "static/css", "/static/css")}
)


public_key, private_key = rsa.newkeys(1024)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rsa", methods=["GET"])
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


@app.route("/hill-cipher", methods=["GET", "POST"])
def hillcipher():
    # holy shit this works
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        text = request.args.get("text", "")
        response = {
            "output": f"(HILL-CIPHER:{text})",
            "steps": render_template("ciphers/learn/hill-cipher.html", text=text),
        }
        print(f"\n{response}\n")
        return jsonify(response)
    else:
        return render_template("ciphers/hill-cipher.html")


if __name__ == "__main__":
    app.run(debug=True)
