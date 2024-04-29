''' This module contains the routes for the ScrapeController class and scraping endpoints.

It contains routes for scraping patches and stats, which are used to scrape League of Legends patch notes and statistics for professional play.

Example usage:
    POST /api/scrape/patches
    POST /api/scrape/stats

Contributors:
    Sam Sui
    Jovi Yoshioka
'''

# Internal imports
from app.controllers import ScrapeController

# Third-party libraries
from flask import Blueprint, jsonify

scrape_blueprint = Blueprint('scrape', __name__, url_prefix='/api/scrape')
scrape_controller = ScrapeController()

@scrape_blueprint.route('/patches', methods=['POST'])
def scrape_patches():
    ''' Scrapes League of Legends patch notes and inserts the data into the MongoDB database.

    Returns:
        JSON: The Reponse object for success or failure.

    '''
    response, status_code = scrape_controller.scrape_patches_and_insert()
    return jsonify(response), status_code

@scrape_blueprint.route('/stats', methods=['POST'])
def scrape_stats():
    ''' Scrapes League of Legends statistics for professional play and inserts the data into the MongoDB database.

    Returns:
        JSON: The Reponse object for success or failure.
    '''

    response, status_code = scrape_controller.scrape_stats_and_insert()
    return jsonify(response), status_code