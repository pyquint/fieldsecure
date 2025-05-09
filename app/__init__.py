from flask import Flask
from sassutils.wsgi import SassMiddleware

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)
    app.wsgi_app = SassMiddleware(
        app.wsgi_app, {"app": ("static/sass", "static/css", "/static/css")}
    )

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.ciphers import bp as ciphers_bp

    app.register_blueprint(ciphers_bp, url_prefix="/ciphers")

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    from app.filters import bp as filters_bp

    app.register_blueprint(filters_bp)

    # might move to dedicated file
    # does not work: https://stackoverflow.com/a/5223810
    app.jinja_env.globals.update(zip=zip)

    return app
