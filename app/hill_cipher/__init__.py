from flask import Blueprint

bp = Blueprint("hill_cipher", __name__)

from app.hill_cipher import routes
