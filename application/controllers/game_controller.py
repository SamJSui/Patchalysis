

#Internal imports
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
        self.beautiful_soup = BeautifulSoupService()
        self.mongo_service = MongoService()

    def get_patches(self):
        ''' Retrieves a list of all patches from the MongoDB collection.

        Returns:
            list: The list of patches.
        '''
        
        try:
            patches = self.beautiful_soup.patches
            return { 'patches': patches }, 200
        except Exception as e:
            return { 'error': f'Failed to retrieve patches: {e}' }, 500

    def get_patch_notes(self, patch_version: str):
        ''' Retrieves a patch notes document from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.

        Returns:
            dict: The retrieved document.
        '''
        
        # Clean up the patch version string
        if '.' in patch_version:
            patch_version = patch_version.replace('.', '_')

        if 'v' in patch_version:
            patch_version = patch_version.replace('v', 'V')
        
        try:
            patch_notes = self.mongo_service.fetch_patch_notes(patch_version)
            return patch_notes, 200
        except Exception as e:
            return { 'error': f'Failed to retrieve patch notes: {e}' }, 500
    
    def get_patch_notes_champion(self, patch_version: str, champion_name: str):
        ''' Retrieves a patch notes document for a specific champion from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.
            champion_name (str): The champion name to retrieve.

        Returns:
            dict: The retrieved document.
        '''
        if '.' in patch_version:
            patch_version = patch_version.replace('.', '_')
        if 'v' in patch_version:
            patch_version = patch_version.replace('v', 'V')
        
        try:
            patch_notes = self.mongo_service.fetch_patch_notes_champion(patch_version, champion_name)
            return patch_notes, 200
        except Exception as e:
            return { 'error': f'Failed to retrieve patch notes: {e}' }, 500
    
    def get_patch_stats(self, patch_version: str):
        ''' Retrieves a patch stats document from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        # Clean up the patch version string
        if '.' in patch_version:
            patch_version = patch_version.replace('.', '_')
        if 'v' in patch_version or 'V' in patch_version:
            patch_version = patch_version[1:]
        
        try:
            patch_stats = self.mongo_service.fetch_patch_stats(patch_version)
            return patch_stats, 200
        except Exception as e:
            return { 'error': f'Failed to retrieve patch notes: {e}' }, 500
    
    def get_patch_stats_champion(self, patch_version: str, champion_name: str):
        ''' Retrieves a patch stats document for a specific champion from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.
            champion_name (str): The champion name to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        # Clean up the patch version string
        if '.' in patch_version:
            patch_version = patch_version.replace('.', '_')
        if 'v' in patch_version or 'V' in patch_version:
            patch_version = patch_version[1:]
        
        try:
            patch_stats = self.mongo_service.fetch_patch_stats_champion(patch_version, champion_name)
            return patch_stats, 200
        except Exception as e:
            return { 'error': f'Failed to retrieve patch notes: {e}' }, 500