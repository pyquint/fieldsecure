from flask import render_template

from app.main import bp


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@bp.route("/invertible-matrix", methods=["GET", "POST"])
def invertible_matrix():
    return render_template("learn/invertible-matrix.html")
