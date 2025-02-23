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


@app.route("/rsa", methods=["GET", "POST"])
def rsa():
    return render_template("ciphers/rsa.html")


@app.route("/hill-cipher", methods=["GET", "POST"])
def hillcipher():
    return render_template("ciphers/hill-cipher.html")


if __name__ == "__main__":
    app.run(debug=True)
