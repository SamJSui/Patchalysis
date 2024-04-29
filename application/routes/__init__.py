''' This module contains the routes for the application.

The routes in this module define the endpoints for the application's API.
'''

from .health_routes import health_blueprint
from .scrape_routes import scrape_blueprint