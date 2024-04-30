''' This module is responsible for handling the routes for the health check of the application.

It contains a route for the health check of the application.

Example usage:

    GET /api/health
'''

# Internal imports
from application.controllers import HealthController

# Third-party libraries
from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__, url_prefix='/api')
health_controller = HealthController()

@health_blueprint.route('/healthcheck', methods=['GET'])
def health_check():
    ''' Checks the health of the application.

    Returns:
        JSON: The Response object for the health check.
    '''
    response, status_code = health_controller.health_check()
    return jsonify(response), status_code