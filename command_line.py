import cmd
import json
import logging

from config_genie import ConfigGenie
from phantom_data_manager import PhantomDataManager
from virtual_event_gen import VirtualEventGen
from export_manager import ExportManager
from log_config import setup_logging

# TODO: implement do_update method

class PyEventGenShell(cmd.Cmd):
    intro = f"Welcome to the PyEventGen shell! Type help or ? to list commands\n"
    #    prompt = f"pegsh > "
    #    prompt = f"peg-sh > "
    #    prompt = f"peg sh > "
    #    prompt = f"pe-sh > "
    #    prompt = f"pyeventgen > "
    prompt = f"(pyeventgen) "

    def __init__(self):
        super().__init__()  # https://stackoverflow.com/questions/22261615/attribute-error-has-no-attribute-completekey-python
        self.config_manager = ConfigGenie()
        self.data_manager = PhantomDataManager()
        self.event_manager = VirtualEventGen(self.config_manager, self.data_manager)
        self.export_manager = ExportManager()

        setup_logging()
        self.logger = logging.getLogger("PyEventGenShell")
        self.logger.info("PyEventGenShell component initialized.")

# Auxiliar functions
    def collection_exists(self, collection):
        """
        Verifies that collection exists
        :param collection: Collection
        :return: (bool)
        """

        if not collection.strip() in self.data_manager.collections:
            print(f"Collection {collection} doesn't exist.")
            self.logger.error("Collection verification failed.")
            return False
        self.logger.info(f"Collection '{collection}' successfully verified.")
        return True

    def verify_arguments(self, args, num_arg, error_prompt):
        """
        Verify the given args meets the minimum requirements for the function to work
        :param args: Given args by the user
        :param num_arg: Number of args required for the function to work
        :param error_prompt: Error message to prompt
        :return: Boolean
        """

        if len(args) != num_arg:
            print(error_prompt)
            self.logger.error("Arguments verification failed.")
            return False
        self.logger.info(f"Arguments verification succeeded.")
        # logger.debug("... args, num_arg ...")
        return True

    def verify_integer(self, number, prompt):
        """
        Verifies that the given integer is valid.
        :param number: Count
        :param prompt: Error message to prompt
        :return: (bool, int) where bool indicates if the integer is valid, and int is the count
        """

        try:
            count = int(number.strip())
        except ValueError:
            print(prompt)
            self.logger.error("Integer validation failed.")
            return False, None
        self.logger.info("Integer validation succeeded.")
        return True, count

    def validate_query(self, query_str):
        """
        Validates if the query is valid and in JSON format
        :param query_str: The query string passed in the command
        :return: (bool, dict) where bool indicates if the query is valid, and dict is the query in JSON format
        """

        try:
            query = json.loads(query_str.strip())
        except json.JSONDecodeError:
            print("Invalid query. Please provide with a valid query in the form of JSON dictionary")
            self.logger.error("Query validation failed.")
            return False, None
        self.logger.info("Query validation succeeded")
        return True, query

    # Command Functions

    def do_init(self, arg):
        """
        Initialize the system configuration (NOT in use yet)
        Usage: init <config>
        :param arg: [string] Config's name
        """

        # Verifies number of arguments passed
        args = arg.split()
        if not self.verify_arguments(args, 1, "Usage: init <config>"):
            return

        # Sets given parameter as the configuration
        config = args[0].strip()
        self.logger.info("Configuration initialized.")

    def do_create_users(self, arg):
        """
        Create phantom users with the given parameters.
        Usage: create_users <count> <username> <role> <group> ...
        :param arg: [int] Count of users to create, [String] Username, [String] User's role, [String] User's Group
        """

        # Verifies number of arguments passed
        args = arg.split()
        if not self.verify_arguments(args, 4, "Usage: create_users <count> <username> <role> <group>"):
            return

        # Verifies 'count' is a valid integer
        is_valid, count = self.verify_integer(args[0], "Invalid number of users. Please enter a valid integer.")
        if not is_valid:
            return

        # Assigns given strings to their variables
        name = args[1].strip()
        role = args[2].strip()
        group = args[3].strip()

        # TODO: should I eliminate this? or it might be used...
        # Verifies that at least one server exist for the selected group
        #servers = self.data_manager.read_doc("servers", {})
        #if len(list(servers)) <= 0:
        #   print(f"Error: No servers available. Please create at least one server before creating users.")
        #   return

        print(f"Creating {count} users...")
        for i in range(1, count+1):
            self.data_manager.create_doc("users",
                                         {"username": f"{name}_{i}", "role": role, "group": group, "active_hours": "8:00-17:00"})
        self.logger.info(f"{count} users created successfully.")
        print(f"{count} users created successfully.")

    #def do_create_user(self, arg):
    #    self.do_create_users(arg)

    def do_create_servers(self, arg):
        """
            Create phantom servers with the given parameters
            Usage: create_servers <count> <server_name> <group_name>
            :param arg: [int] Number of servers to create, [string] Server's name, [string] Group's name
            """

        # Verifies number of arguments passed
        args = arg.split()
        if not self.verify_arguments(args, 3, "Usage: create_servers <count> <server_name> <group_name>"):
            return

        # Verifies provided count is a valid integer
        server_name = args[1]
        is_valid, count = self.verify_integer(args[0], "Invalid number of servers. Please enter a valid integer.")
        if not is_valid:
            return

        # TODO: verify that group exists, if doesn't exist, create a new one with default values
        group = args[2].strip()

        print(f"Creating {count} servers...")
        for i in range(1, count+1):
            self.data_manager.create_doc("servers",
                                         {"server_name": f"{server_name}_{i}", "server_type": "web", "group": group})
        self.logger.info(f"{count} servers created successfully.")
        print(f"{count} servers created successfully.")

    #def do_create_server(self, arg):
    #    self.do_create_servers(arg)

    def do_read(self, arg):
        """
        Reads documents from a specified collection based on a query.
        Usage: read <collection> <query>
        Examples of usage:
        - read servers {} : Shows all servers.
        - read servers {group: "apache"} : shows all servers where the field group is "apache"
        :param arg: [String] Collection name, [Dict] Query in JSON format
        """

        # Verifies the number of arguments passed
        args = arg.split(maxsplit=1)
        if not self.verify_arguments(args, 2, "Usage: read <collection> <query>"):
            return

        # Verifies collection exists in current db
        collection = args[0]
        if not self.collection_exists(collection):
            return

        # Verifies that the query is a valid dictionary
        # Uses a tuple, to know if query is valid, and store the query
        query_str = args[1]
        is_valid, query = self.validate_query(query_str)
        if not is_valid:
            return

        # Converts returned cursor into a list,
        # and print each document on the list
        cursor = self.data_manager.read_doc(collection, query)
        results = list(cursor)
        if results:
            for document in results:
                print(document)
            self.logger.info("Documents were successfully read.")
        else:
            print("No documents found with the given collection and query.")

    def do_remove(self, arg):
        """
            Removes documents from a specified collection based on a query.
            Usage: remove <collection> <query>
            Examples of usage:
            - remove servers {} : Removes all servers.
            - removes servers {group: "apache"} : Removes all servers where the field group is "apache"
            :param arg: [String] Collection name, [Dict] Query in JSON format
        """

        # Verifies the number of arguments passed
        args = arg.split(maxsplit=1)
        if not self.verify_arguments(args, 2, "Usage: remove <collection> <query>"):
            return

        # Verifies collection exists in current db
        collection = args[0]
        if not self.collection_exists(collection):
            return

        # Verifies that the query is a valid dictionary
        query_str = args[1]
        is_valid, query = self.validate_query(query_str)
        if not is_valid:
            return

        # Assigns the cursor to a variable and verifies if it has documents
        cursor = self.data_manager.read_doc(collection, query)
        if not cursor:
            print("No documents found.")
            return

        # Shows the list of documents to be deleted
        print("The following documents will be deleted:")
        self.do_read(arg)

        # Gets confirmation from the user
        if not self.get_confirmation():
            return

        # Removes the documents
        self.data_manager.remove_doc(collection, query)
        print(f"Documents removed!")
        self.logger.info("Documents successfully removed.")

    def do_generate_events(self, arg):
        """
        Generate and exports events based on the given parameters.
        Usage: generate_events <count> <servers_query> <users_query> <export_format>

        Export format: [json, log, none], (csv, xml) -> to be implemented
        Event type: [random, or a string] to be implemented

        Examples of usage:
        - generate 100 {} {} json : Generates 100 events filtering by all servers and users, and exports them in JSON format.
        - generate 50 {"server_name":apache_1} {"role":"user","group":"sales"} csv : Generates 50 events from server "apache_1" and random users with role "user" and group "sales", and exports them in CSV format.
        - generate 20 {} {"role":"user","group":"test"} none : Generates 50 events from server "apache_1" and random users with role "user" and group "sales" but doesn't export them.
          {} = ALL
        :param arg: [int] Count of events, [Dict] Servers query in JSON format, [Dict] Users query in JSON format, [String] export format
        """

        # Verifies number of arguments passed
        args = arg.split()
        if not self.verify_arguments(args, 4, "Usage: generate_events <count> <servers_query> <users_query> <format>"):
            return

        # Verifies that count is a valid integer
        is_valid, count = self.verify_integer(args[0], "Invalid number of events. Please enter a valid integer.")
        if not is_valid:
            return

        # Validates users and servers query. If queries are valid,
        # they get successfully assigned to variables
        is_valid_s, servers_query = self.validate_query(args[1])
        is_valid_u, users_query = self.validate_query(args[2])
        if not is_valid_s or not is_valid_u:
            return

        # Verifies that the provided format is valid
        format = args[3]
        if not self.export_manager.verify_export_format(format):
            return

        # Verifies that the provided collections and queries sucesfully
        # finds match/documents (If not, it won't be able to generate events)
        servers = self.data_manager.read_doc("servers", servers_query)
        if len(list(servers)) <= 0:
            print(f"No servers found with query {servers_query}.")
            return
        users = self.data_manager.read_doc("users", users_query)
        if len(list(users)) <= 0:
            print(f"No users found with query {users_query}.")
            return

        # For each event generated within the 'for' iteration, the event
        # will be appended to the list events
        print("Generating events...")
        events = []
        for i in range(count):
            event = self.event_manager.generate_event(users_query, servers_query)
            if event:
                events.append(event)
                print(f"{event}")
        print(f"({count}) events generated succesfully!")

        self.logger.info(f"({count}) events generated successfully.")
        self.logger.info(f"Now proceeding to call the export method.")

        # Exports the generated events in 'events' list
        # and exports it in the format specified by the user
        self.export_manager.export(events, format)

    #def do_generate_event(self, arg):
    #    self.do_generate_events(arg)
    # This worked to fix typos from the user, but, it is problematic because
    # appears in the 'help' command as "undocumented commands" and are duplicated.

    def do_exit(self, arg):
        """
        Exit the PyEventGen shell
        Usage: exit
        """

        if self.get_confirmation():
            print("Exiting...")
            self.logger.info(f"Exiting the program (Actioned by user).")
            exit(0)
        else:
            return

    def get_confirmation(self, prompt="Would you like to proceed? (Y/n): "):
        """
        Prints a prompt and asks for confirmation from the user.
        :param prompt: The prompt to be printed.
        :return: Boolean
        """
        confirmation_options = {
            True: {"", "y", "yes", "k", "ok", "yeah", "hell yeah", "hellyeah", "yep", "yiep", "yai"},
            False: {"n", "no", "noup", "nop", "nope", "hell no", "hellno", "no lol", "nolol"}
        }
        while True:
            confirm = input(prompt).strip().lower()
            if confirm in confirmation_options[True]:
                return True
            elif confirm in confirmation_options[False]:
                return False
            else:
                print("Invalid input.")

