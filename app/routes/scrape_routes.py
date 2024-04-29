from flask import Blueprint, request, jsonify, Response

from app.controllers import ScrapeController

scrape_blueprint = Blueprint('scrape', __name__, url_prefix='/api/scrape')
scrape_controller = ScrapeController()

@scrape_blueprint.route('/patches', methods=['POST'])
def scrape_patches():
    ''' Scrapes League of Legends patch notes and returns the scraped data.

    Returns:
        JSON: The Reponse object for success or failure.

    '''
    response = scrape_controller.scrape_patches()
    return jsonify(response[0]), response[1]

@scrape_blueprint.route('/stats', methods=['POST'])
def scrape_stats():
    ''' Scrapes League of Legends statistics for professional play.

    Returns:
        JSON: The Reponse object for success or failure.
    '''

    response = scrape_controller.scrape_stats()
    return jsonify(response[0]), response[1]