import os
from flask import Flask
from flask_restful import Api
from chatbot import db
from chatbot.resources import Question, Bot
from chatbot.bot.client import Client
import atexit


def close_bert_client():
    Client.close()


atexit.register(close_bert_client)


def create_app(test_config=None, name=None):

    """Create and configure an instance of the Flask application."""
    app = Flask(name or __name__, instance_relative_config=True)
    api = Api(app, catch_all_404s=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "database.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    db.init_app(app)

    # # Warmup the bert client
    Client.warmup(app)

    # # Register REST endpoints
    api.add_resource(Question, '/questions')
    api.add_resource(Bot, '/bot')

    return app
