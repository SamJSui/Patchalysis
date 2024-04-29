''' This file is used to import all the services in the services folder. 

This allows for cleaner imports in other modules, as shown in the examples above.

Classes:
    BeautifulSoupService: A class for scraping data from the web using BeautifulSoup.
    MongoService: A class for interacting with MongoDB.

Contributors:
    Sam Sui
    Jovi Yoshioka
'''

from .beautiful_soup_service import BeautifulSoupService
from .mongo_service import MongoService