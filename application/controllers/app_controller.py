
# Internal imports
from application.services.beautiful_soup_service import BeautifulSoupService
from application.services.mongo_service import MongoService

# Standard libraries

# Third-party libraries

class GameController:
    ''' The GameController class is responsible for handling requests related to the game data.

    Attributes:
        beautiful_soup (BeautifulSoup): The BeautifulSoup instance used to parse HTML.
        mongo_service (MongoService): The MongoService instance used to interact with the MongoDB database.

    '''

    def __init__(self):
        pass