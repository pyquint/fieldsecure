import rsa
from flask import Flask, render_template, request
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {"fieldsecure": ("static/sass", "static/css", "/static/css")}
)


public_key, private_key = rsa.newkeys(1024)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    key = request.args.get("key", "")
    method = request.args.get("method", "rsa")

    input_text, output_text = "", ""

    return render_template("encrypt.html")


if __name__ == "__main__":
    app.run(debug=True)
