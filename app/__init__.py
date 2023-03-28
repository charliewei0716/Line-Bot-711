from flask import Flask
from decouple import config

def create_app():

    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = config("CONFIG_TYPE")
    app.config.from_object(CONFIG_TYPE)

    # Register blueprints
    register_blueprints(app)

    return app


def register_blueprints(app: Flask):
    from app.bot import bot_blueprint
    app.register_blueprint(bot_blueprint, url_prefix='/bot')