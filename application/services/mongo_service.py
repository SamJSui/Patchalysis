''' This module provides a service for interacting with MongoDB.

It contains a class `MongoService` that encapsulates the functionality to connect to a MongoDB database,
insert documents into collections, and handle exceptions.

Example usage:
    mongo_service = MongoService()
    mongo_service.insert_one('users', {'name': 'John Doe', 'age': 30})

Classes:
    MongoService: A class for interacting with MongoDB.

Attributes:
    logger: A logger object for logging messages.

Contributors:
    Sam Sui
'''

# Standard libraries
import os
import logging

# Third-party libraries
from pymongo.mongo_client import MongoClient
from pymongo import errors

class MongoService:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoService, cls).__new__(cls)

            # MongoDB Connection Singleton
            cls._instance.uri = os.getenv('MONGO_URI')
            cls._instance.client = MongoClient(
                cls._instance.uri,
                ssl=True,
                ssl_cert_reqs=False # Resolves TLS error
            )
            cls._instance.db = cls._instance.client['Patchalaysis']
        return cls._instance

    def __init__(self):
        ''' Initializes a new instance of the `MongoService` class.

        It establishes a connection to the MongoDB database using the provided environment variable `MONGO_URI`.
        If the connection is successful, it sets the `client` and `db` attributes.

        Raises:
            Exception: If failed to connect to MongoDB.
        '''

        self.logger = logging.getLogger(__name__)

    def fetch_patch_notes(self, patch_version: str):
        ''' Retrieves a patch notes document from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        try:
            collection = self.db['patches']
            result = collection.find_one(patch_version)
            self.logger.info(f"Document retrieved successfully: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to retrieve document: {e}")
            return None
        
    def fetch_patch_notes_champion(self, patch_version: str, champion_name: str):
        ''' Retrieves a patch notes document for a specific champion from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.
            champion_name (str): The champion name to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        try:
            collection = self.db['patches']
            result = collection.find_one({ 'version': patch_version, 'champion': champion_name })
            self.logger.info(f"Document retrieved successfully: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to retrieve document: {e}")
            return None

    def fetch_patch_stats(self, patch_version: str):
        ''' Retrieves a patch stats document from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        try:
            collection = self.db['stats']
            result = collection.find_one(patch_version)
            self.logger.info(f"Document retrieved successfully: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to retrieve document: {e}")
            return None

    def fetch_patch_stats_champion(self, patch_version: str, champion_name: str):
        ''' Retrieves a patch stats document for a specific champion from the MongoDB collection.

        Args:
            patch_version (str): The patch version to retrieve.
            champion_name (str): The champion name to retrieve.

        Returns:
            dict: The retrieved document.
        '''

        try:
            collection = self.db['stats']
            result = collection.find_one({ 'version': patch_version, 'champion': champion_name })
            self.logger.info(f"Document retrieved successfully: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to retrieve document: {e}")
            return None

    def insert_one(self, collection_name, document):
        ''' Inserts a single document into the specified MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to insert.

        Returns:
            str: The inserted document's ID.

        Raises:
            Exception: If failed to insert the document.
        '''

        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            self.logger.info(f"Document inserted successfully: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to insert document: {e}")
            return None

    def insert_many(self, collection_name, documents):
        ''' Inserts multiple documents into the specified MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            documents (list): A list of dictionaries representing the documents to insert.

        Returns:
            list: The inserted documents' IDs.

        Raises:
            Exception: If failed to insert the documents.
        '''

        try:
            collection = self.db[collection_name]
            result = collection.insert_many(documents)
            self.logger.info(f"Documents inserted successfully: {result.inserted_ids}")
            return result.inserted_ids
        except errors.BulkWriteError as bwe:
            print("Error inserting documents:")
            for error in bwe.details['writeErrors']:
                print(f"Index: {error['index']} - {error['errmsg']}")
        except Exception as e:
            self.logger.error(f"Failed to insert documents: {e}")
            return None
