from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    
    
    # Creating app configurations
    app.config.from_object(config_options[config_name])
    
    
    return app
