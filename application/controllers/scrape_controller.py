''' Controller class for scraping patches and stats.

This module contains the ScrapeController class, which is responsible for handling the logic for scraping patches and stats.

Classes:
    ScrapeController: A controller class for scraping patches and stats.

Contributors:
    Sam Sui
    Jovi Yoshioka
'''

# Internal imports
from app.services import BeautifulSoupService
from app.services import MongoService

# Third-party libraries
from flask import request

class ScrapeController:
    ''' Controller class for scraping patches and stats.
    '''

    def __init__(self):
        self.scrape_service = BeautifulSoupService()
        self.mongo_service = MongoService()

    def scrape_patches_and_insert(self):
        ''' Scrapes patches using the scrape_service.

        Returns:
            A tuple containing the success message and status code.
        '''
        
        try:
            scraped_patches = self.scrape_service.scrape_patches()
            self.mongo_service.insert_many('patches', scraped_patches)
            return { 'message': 'Successfully scraped patches' }, 200
        except Exception as e:
            return { 'error': str(e) }, 500

    def scrape_stats_and_insert(self):
        ''' Scrapes stats using the scrape_service.

        Returns:
            A tuple containing the success message and status code.
        '''

        try:
            scraped_stats = self.scrape_service.scrape_stats()
            self.mongo_service.insert_many('stats', scraped_stats)
            return { 'message': 'Successfully scraped stats' }, 200
        except Exception as e:
            return { 'error': str(e) }, 500