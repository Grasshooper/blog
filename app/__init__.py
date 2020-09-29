from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap

def create_app(config_name):

    #Initialize app
    app= Flask(__name__)

    # Setting up configuration
    app.config.from_object(config_options[config_name])
   
    # Initializing Flask Extensions
    bootstrap = Bootstrap(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

