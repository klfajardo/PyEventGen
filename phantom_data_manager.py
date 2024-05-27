import logging
from pymongo import MongoClient

# TODO: Dig more about checks, predicates, error handling, etc... for CRUD operations

class PhantomDataManager:
    def __init__(self, uri="mongodb://localhost:27017/", dbname="phantom_data_db"):
        self.collections_allowed = {
            "servers",
            "users",
            #"ips"
        }

        # Creates the Mongo connection using a variable/constant that references LOCALHOST.
        self.client = MongoClient(uri)

        # Initializes database
        # If doesn't exist, mongo creates one
        self.db = self.client[dbname]

        # Dictionary contains every collection of the database used by this app.
        self.collections = {}
        # For each member in CollectionsAllowedEnum, creates an entry in the dictionary
        for collection in self.collections_allowed:
            collection_name = collection
            collection_mongo = self.db[collection_name]
            # Creates an entry on the dictionary ["name" mongo]
            self.collections[collection_name] = collection_mongo

        self.logger = logging.getLogger("PhantomDataManager")
        self.logger.info(f"Initialized PhantomDataManager with DB: name={dbname} uri={uri}")

    # AUXILIARY FUNCTIONS
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
        self.collections[collection].update_one(query, {"$set": new_values})
        self.logger.info(
            f"Documents filtered by '{query}' query in collection '{collection}' were updated. Old value: '{old_values}' New value: '{new_values}'")

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
    import logging
from pymongo import MongoClient

# TODO: Dig more about checks, predicates, error handling, etc... for CRUD operations

class PhantomDataManager:
    def __init__(self, uri="mongodb://localhost:27017/", dbname="phantom_data_db"):
        self.collections_allowed = {
            "servers",
            "users",
            #"ips"
        }

        # Creates the Mongo connection using a variable/constant that references LOCALHOST.
        self.client = MongoClient(uri)

        # Initializes database
        # If doesn't exist, mongo creates one
        self.db = self.client[dbname]

        # Dictionary contains every collection of the database used by this app.
        self.collections = {}
        # For each member in CollectionsAllowedEnum, creates an entry in the dictionary
        for collection in self.collections_allowed:
            collection_name = collection
            collection_mongo = self.db[collection_name]
            # Creates an entry on the dictionary ["name" mongo]
            self.collections[collection_name] = collection_mongo

        self.logger = logging.getLogger("PhantomDataManager")
        self.logger.info(f"Initialized PhantomDataManager with DB: name={dbname} uri={uri}")

    # AUXILIARY FUNCTIONS
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
        self.collections[collection].update_one(query, {"$set": new_values})
        self.logger.info(
            f"Documents filtered by '{query}' query in collection '{collection}' were updated. Old value: '{old_values}' New value: '{new_values}'")

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
