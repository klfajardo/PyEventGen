import logging
from pymongo import MongoClient, errors
from colors import Colors
import time


class PhantomDataManager:

    def __init__(self):
        self.collections_allowed = {
            "servers",
            "users",
            # "ips"
        }
        self.logger = logging.getLogger("PhantomDataManager")

        # Initialize MongoDB client and database
        self.client = None
        self.db = None
        self.request_uri()
        self.request_db_name()

        # Dictionary contains every collection of the database used by this app.
        self.collections = {}
        # For each member in collections_allowed, creates an entry in the dictionary
        for collection in self.collections_allowed:
            collection_name = collection
            collection_mongo = self.db[collection_name]
            # Creates an entry on the dictionary ["name" mongo]
            self.collections[collection_name] = collection_mongo

        self.logger.info(f"Initialized PhantomDataManager component.")
        time.sleep(1.5)

    # AUXILIARY FUNCTIONS

    def request_uri(self):
        """
        Requests to the user the mongodb URI to connect.
        """

        default_uri = "mongodb://localhost:27017/"
        while True:
            uri = (input(f"Enter {Colors.ORANGE}MongoDB URI{Colors.ENDC} (default: mongodb://localhost:27017/):\n> ")
                   or default_uri)
            is_valid, message = self.verify_mongodb_uri(uri)
            print(message)
            self.logger.info(message)
            if is_valid:
                self.logger.info(f"MongoDB URI verified successfully.")
                return

    def request_db_name(self):
        """
        Requests to the user the mongodb database name to connect.
        """

        default_db = "phantom_data_db"
        while True:
            db = input(f"Enter {Colors.ORANGE}MongoDB database name{Colors.ENDC} (default: phantom_data_db)\n"
                       f"If it does not exist, one will be created with the given name\n> ") or default_db
            is_valid, message = self.verify_mongodb_db(db)
            print(message)
            self.logger.info(message)
            if is_valid:
                self.logger.info(f"MongoDB db verified successfully.")
                return

    def verify_mongodb_uri(self, uri):
        """
        Uses the provided URI to attempt a connection to the MongoDB server.
        Catches any exceptions that occur during the connection attempt.
        :param uri: [String] Provided URI
        :return: [Tuple] Boolean, Returned message
        """

        try:
            # Attempt to create a client and list the databases
            self.client = MongoClient(uri, serverSelectionTimeoutMS=10000)  # 10 seconds
            self.client.server_info()  # Force connection on a request as the ping is lazily connected
            return True, f"{Colors.OKGREEN}Connection successful!{Colors.ENDC}"
        except errors.ServerSelectionTimeoutError:
            return False, "Server selection timeout. Could not connect to the server."
        except errors.ConnectionFailure:
            return False, "Connection failure. Could not connect to the server."
        except errors.InvalidURI:
            return False, "Invalid URI. The URI provided is incorrect."
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"

    def verify_mongodb_db(self, db):
        """
        Attempts to connect to the specified database within the MongoDB server.
        Catches any exceptions that occur during the connection attempt.
        :param db:
        :return: [Tuple] Boolean, Returned message
        """

        try:
            # Initialize db
            self.db = self.client[db]
            # Try to list collections to ensure the database is accessible.
            self.db.list_collection_names()
            return True, f"{Colors.OKGREEN}Database connection successful!{Colors.ENDC}"
        except errors.OperationFailure:
            return False, "Database operation failed. Could not access the database."
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"

    def exists_collection(self, collection):
        """
        # Verifies that given collection exists and is allowed in the db
        :param collection: Given collection
        :return: Boolean
        """

        if collection not in self.collections:
            self.logger.error(
                "Tried to insert document '{document}' into collection '{collection}'. Collection doesn't exist.")
            return False
        return True

    # CRUD OPERATIONS
    # https://www.mongodb.com/docs/manual/crud/#create-operations

    def create_doc(self, collection, document):
        """
        Add given documents to a collection.
        :param collection: [String] Name of the collection.
        :param document: [Dictionary] Document to be inserted.
        """

        # Verifies that given collection exists and is allowed in the db
        if not self.exists_collection(collection):
            return

        # Insert document into collection
        self.collections[collection].insert_one(document)
        print(document)
        self.logger.info(f"Document '{document}' inserted in collection '{collection}'.")

    def read_doc(self, collection, query):
        """
        Reads documents found from the given collection and query.
        :param collection: [String] Name of the collection.
        :param query: [Dictionary] Query to find the document(s)
        :return: Documents
        """

        # Verifies that given collection exists and is allowed in the db
        if not self.exists_collection(collection):
            return

        # Read document from collection
        self.logger.info(f"Document(s) filtered by '{query}' query in collection '{collection}' has been read.")
        return self.collections[collection].find(query)

    def update_doc(self, collection, query, new_values):
        """
        Updates document(s) found with the given query in the given collection.
        :param collection: [String] Name of the collection.
        :param query: [Dictionary] Query to find the document(s).
        :param new_values: [Dictionary] New values for the document(s).
        """

        # Verifies that given collection exists and is allowed in the db
        if not self.exists_collection(collection):
            return

        # Saves old document value for logging (or to restore a change)
        old_values = self.read_doc(collection, query)

        # Update document from collection
        # self.collections[collection].update_many(query, new_values)

        self.collections[collection].update_many(query, {"$set": new_values})
        self.logger.info(
            f"Documents filtered by '{query}' query in collection '{collection}' were updated. "
            f"Old value: '{old_values}' New value: '{new_values}'")

    def remove_doc(self, collection, query):
        """
        Removes documents found with the given query in the given collection.
        :param collection: [String] Name of the collection.
        :param query: [Dictionary] Query to find the document(s).
        """

        # Verifies that given collection exists and is allowed in the db
        if not self.exists_collection(collection):
            return

        # Delete document from collection
        self.collections[collection].delete_many(query)
        self.logger.info(f"Document(s) filtered by '{query}' query in collection '{collection}' has been removed.")
