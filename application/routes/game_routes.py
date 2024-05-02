


# Internal imports
from application.controllers import GameController

# Third-party libraries
from flask import Blueprint, jsonify

game_blueprint = Blueprint('game', __name__, url_prefix='/api')
game_controller = GameController()

@game_blueprint.route('/patch_notes/<patch_version>', methods=['GET'])
def get_patch_notes(patch_version):
    ''' Retrieves a patch notes document from the MongoDB collection.

    Args:
        patch_version (str): The patch version to retrieve.

    Returns:
        JSON: The retrieved document.
    '''

    response, status_code = game_controller.get_patch_notes(patch_version)
    return jsonify(response), status_code

@game_blueprint.route('/patch_notes/<patch_version>/<champion_name>', methods=['GET'])
def get_patch_notes_champion(patch_version, champion_name):
    ''' Retrieves a patch notes document for a specific champion from the MongoDB collection.

    Args:
        patch_version (str): The patch version to retrieve.
        champion_name (str): The champion name to retrieve.

    Returns:
        JSON: The retrieved document.
    '''

    response, status_code = game_controller.get_patch_notes_champion(patch_version, champion_name)
    return jsonify(response), status_code

@game_blueprint.route('/patch_stats/<patch_version>', methods=['GET'])
def get_patch_stats(patch_version):
    ''' Retrieves a patch stats document from the MongoDB collection.

    Args:
        patch_version (str): The patch version to retrieve.

    Returns:
        JSON: The retrieved document.
    '''

    response, status_code = game_controller.get_patch_stats(patch_version)
    return jsonify(response), status_code

@game_blueprint.route('/patch_stats/<patch_version>/<champion_name>', methods=['GET'])
def get_patch_stats_champion(patch_version, champion_name):
    ''' Retrieves a patch stats document for a specific champion from the MongoDB collection.

    Args:
        patch_version (str): The patch version to retrieve.
        champion_name (str): The champion name to retrieve.

    Returns:
        JSON: The retrieved document.
    '''

    response, status_code = game_controller.get_patch_stats_champion(patch_version, champion_name)
    return jsonify(response), status_code