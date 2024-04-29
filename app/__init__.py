from flask import Flask
from app.routes import health_blueprint  # Assuming health_routes defines a Blueprint
from app.routes import scrape_blueprint  # Assuming scrape_routes defines a Blueprint

def create_app():
    ''' Create a Flask application using the app factory pattern.

    Returns:
        Flask: The created Flask application.
    '''
    app = Flask(__name__)
    
    app.register_blueprint(health_blueprint)
    app.register_blueprint(scrape_blueprint)

    return app