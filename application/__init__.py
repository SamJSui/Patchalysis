from flask import Flask
from application.routes import game_blueprint 
from application.routes import health_blueprint 
from application.routes import scrape_blueprint
from application.routes import app_blueprint


def create_app():
    ''' Create a Flask application using the app factory pattern.

    Returns:
        Flask: The created Flask application.
    '''
    app = Flask(__name__, static_url_path='/static')

    # Register blueprints
    app.register_blueprint(game_blueprint)
    app.register_blueprint(health_blueprint)
    app.register_blueprint(scrape_blueprint)
    app.register_blueprint(app_blueprint)

    return app


application = create_app()