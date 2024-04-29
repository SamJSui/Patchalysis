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
from pymongo import MongoClient

class MongoService:
    def __init__(self):
        '''
        Initializes a new instance of the `MongoService` class.

        It establishes a connection to the MongoDB database using the provided environment variable `MONGO_URI`.
        If the connection is successful, it sets the `client` and `db` attributes.

        Raises:
            Exception: If failed to connect to MongoDB.
        '''
        self.logger = logging.getLogger(__name__)
        
        try:
            self.uri = os.getenv('MONGO_URI')
            self.client = MongoClient(self.uri)
            self.db = self.client['Patchalysis']
            self.logger.info("MongoDB connection established successfully.")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")

    def insert_one(self, collection_name, document):
        '''
        Inserts a single document into the specified MongoDB collection.

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

    def insert_many(self, collection_name, documents):
        '''
        Inserts multiple documents into the specified MongoDB collection.

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
        except Exception as e:
            self.logger.error(f"Failed to insert documents: {e}")
            return None
