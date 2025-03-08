from flask import Blueprint

bp = Blueprint("rsa", __name__)

from app.rsa import routes
