from flask import request
from app.services import BeautifulSoupService

class ScrapeController:
    ''' Controller class for scraping patches and stats.
    '''

    def __init__(self):
        self.scrape_service = BeautifulSoupService()

    def scrape_patches(self):
        ''' Scrapes patches using the scrape_service.

        Returns:
            A tuple containing the success message and status code.
        '''
        
        try:
            self.scrape_service.scrape_patches()
            return 'Successfully scraped patches', 200
        except Exception as e:
            return str(e), 500

    def scrape_stats(self):
        ''' Scrapes stats using the scrape_service.

        Returns:
            A tuple containing the success message and status code.
        '''

        try:
            self.scrape_service.scrape_stats()
            return 'Successfully scraped stats', 200
        except Exception as e:
            return str(e), 500