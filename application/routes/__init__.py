''' This module contains the routes for the application.

The routes in this module define the endpoints for the application's API.
'''

from .game_routes import game_blueprint
from .health_routes import health_blueprint
from .scrape_routes import scrape_blueprint
from .app_routes import app_blueprint