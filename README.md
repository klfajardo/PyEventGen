# PyEventGen
PyEventGen is a flexible and open-source tool designed for generating fictitious events, intended to simulate traffic and activity on information and event monitoring systems. It is especially useful for developers and system administrators who need to generate simulated data for software testing or training on monitoring tools like SIEM.

# Features
- Dynamic generation of fictitious events based on user-defined queries.
- Integration with MongoDB to effectively manage and manipulate data.
- Event export in multiple formats including JSON and log records, with future implementations for XML, CSV and others.
- Configuration and management of users and servers through an interactive console.
- Logging system to monitor and record operations performed by the system.

# Why is this project useful?
- By simulating a variety IT security events, this tool enables users to rigorously test how their SIEM systems and other monitoring tools respond to varied and complex scenarios.
- The tool can generate large volumes of simulated events quickly, allowing users to test and stress their systems without the need for real data.
- Programmers can use this tool to understand better how to interact with databases like MongoDB, implement CRUD operations, and develop efficient data parsing techniques.
- The tool provides a fictitious sandbox environment for experimenting with data structures, algorithms, and system design. This is particularly useful for students and professionals in computer science who need a practical way to apply theoretical concepts.
- Users can customize the types and volumes of data generated, making it a flexible tool for various testing and development needs.

# How do I get started?
## Installation
Clone this repository using:
```
git clone https://github.com/klfajardo/PyEventGen
```
Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

To start the interactive console of PyEventGen:
```
python command_line.py
```

When the program runs for the first time, it will prompt for a MongoDB connection URI and database name. You can simply press enter to use the default settings if you have MongoDB Community Edition running on your localhost. Any database name you enter will create a new database, allowing you to maintain separate mock environments for various use cases. You can also specify remote URIs to connect to a remote MongoDB server.

### Available Commands

#### `init`

Initialize the system configuration (currently not in use).

#### `create_users`

Create phantom users with the specified parameters.

**Usage**:
```
create_users <count> <username> <role> <group>
```

**Example**:
```
create_users 10 test_user admin dev_team
```
This command creates 10 users with usernames `test_user_1` to `test_user_10`, role `admin`, and group `dev_team`.

#### `create_servers`

Create phantom servers with the specified parameters.

**Usage**:
```
create_servers <count> <server_name> <group_name>
```

**Example**:
```
create_servers 5 test_server prod_team
```
This command creates 5 servers with names `test_server_1` to `test_server_5`, and group `prod_team`.

#### `read`

Read documents from a specified collection based on a query.

**Usage**:
```
read <collection> <query>
```

**Examples**:
```
read servers {}
```
This command reads all documents from the `servers` collection.

```
read users {"role": "admin"}
```
This command reads all documents from the `users` collection where the role is `admin`.

#### `update`

Update documents in a specified collection based on a query.

**Usage**:
```
update <collection> <query> <new_value>
```

**Examples**:
```
update servers {} {"group": "new_group"}
```
This command updates all documents in the `servers` collection to set the group to `new_group`.

```
update users {"username": "test_user_1"} {"role": "super_admin"}
```
This command updates the user `test_user_1` to have the role `super_admin`.

#### `remove`

Remove documents from a specified collection based on a query.

**Usage**:
```
remove <collection> <query>
```

**Examples**:
```
remove servers {}
```
This command removes all documents from the `servers` collection.

```
remove users {"group": "test_team"}
```
This command removes all users in the `test_team` group.

#### `generate_events`

Generate and export events based on the given parameters. Depending on the specified format, a new file with the specified format will be created in the installation directory containing the events.

**Usage**:
```
generate_events <count> <servers_query> <users_query> <export_format>
```

**Examples**:
```
generate_events 100 {} {} json
```
This command generates 100 events using all servers and users, and exports them in JSON format.

```
generate_events 50 {"server_name": "test_server_1"} {"role": "user", "group": "dev_team"} csv
```
This command generates 50 events using `test_server_1` and users with role `user` and group `dev_team`, and exports them in CSV format.

```
generate_events 20 {} {"role": "admin"} none
```
This command generates 20 events using all servers and users with role `admin`, but does not export them.

#### `clear`

Clear the console.

**Usage**:
```
clear
```

#### `exit`

Exit the PyEventGen shell.

**Usage**:
```
exit
```

By following these usage examples, you can effectively utilize the `PyEventGenShell` to manage phantom users and servers, generate events, and export them in various formats.

### Confirmations and Error Handling
Many commands prompt for confirmation before making changes, and all commands include error handling to ensure invalid inputs are managed gracefully. For example, if a query or argument is invalid, an error message will be printed, and the command will not proceed.

Additionally, the program logs all actions and errors to a file named pyeventgen.log in the installation directory. This log file is useful for troubleshooting and understanding what each component of the program is doing.

### MongoDB Connection
As mentioned above, upon the first run, the program will prompt for a MongoDB connection URI and database name. You can press enter to use the default settings if you have MongoDB Community Edition running on your localhost. Any database name you enter will create a new database, allowing you to maintain separate mock environments for various use cases. You can also specify remote URIs to connect to a remote MongoDB server.

As MongoDB is used, if you close the program, exit, or shut down the computer, your data will remain intact as long as MongoDB is running. Ensure you specify the same database name upon restarting the program to access your existing data. You can manage your databases using mongosh or MongoDB Compass for a web interface.

For a visual reference on deploying PyEventGen, please see the PyEventGen deployment visual reference. (will add link here)

# Where can I get more help, if I need it?
Feel free to contact me via email, linkedin or any social media you find me on!

# License
This project is licensed under the GNU General Public License, version 2 - see the LICENSE file for details.

**Thank you so much! Any feedback is greatly appreciated! :)**
