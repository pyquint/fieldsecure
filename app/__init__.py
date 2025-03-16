from flask import Flask
from sassutils.wsgi import SassMiddleware

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)
    app.wsgi_app = SassMiddleware(
        app.wsgi_app, {"app": ("static/sass", "static/css", "/static/css")}
    )

    print("\ncreate_app\n")

    from app.hill_cipher import bp as hill_cipher_bp

    app.register_blueprint(hill_cipher_bp)

    from app.rsa import bp as rsa_cipher_bp

    app.register_blueprint(rsa_cipher_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    app.jinja_env.globals.update(zip=zip)

    return app
