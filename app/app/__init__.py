import os

from flask import Flask
from flask_cors import CORS
import rq_dashboard
from .routes import rest_api
from .jobs import rq


def create_app(app_settings=None):
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    if not app_settings:
        app_settings = os.getenv('APP_SETTINGS', 'app.config.ProductionConfig')
    app.config.from_object(app_settings)

    # register blueprints
    app.register_blueprint(rest_api, url_prefix='/api')
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/dashboard")
    rq.init_app(app)

    return app
