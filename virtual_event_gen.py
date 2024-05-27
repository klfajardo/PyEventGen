import logging
import time
import random

class VirtualEventGen():
    def __init__(self, config_manager, data_manager):
        # Manager components get imported from command_line.py initialization/instantiation
        self.config_manager = config_manager
        self.data_manager = data_manager
        self.logger = logging.getLogger("VirtualEventGen")
        self.logger.info("VirtualEventGen component initialized.")

    def generate_event(self, users_query, servers_query):
        """
        Generates a mock event. One at the time.
        :param users_query: [Dictionary] Filters the users to be used in the event.
        :param servers_query: [Dictionary] Filters the servers to be used in the event.
        :return: Generated event
        """

        # Obtain global config (NOT USED AT THE MOMENT)
        #event_type = self.config_manager.get_global_config("event_type")
        #active_hours = self.config_manager.get_global_config("active_hours")

        # I haven't figured out yet how I'm gonna code this or what the purpose of
        # event_type and active_hours fields is gonna be, so for now, I will just
        # throw a list of possible random event_types, pick one of them every time
        # an event is generated, and hardcode an active hours value.
        event_types = [
            "login_success",
            "login_failure",
            "file_access",
            "file_deletion",
            "file_modification",
            "system_start",
            "system_shutdown",
            "user_creation",
            "user_deletion",
            "user_privilege_change",
            "network_connection",
            "network_disconnection",
            "malware_detection",
            "firewall_rule_change",
            "configuration_change",
            "software_installation",
            "software_uninstallation",
            "service_start",
            "service_stop",
            "backup_creation",
            "backup_restoration",
            "data_export",
            "data_import",
            "security_alert",
            "policy_violation",
            "resource_overuse",
            "database_query",
            "database_update",
            "system_error",
            "hardware_failure",
            "password_change",
            "password_reset",
            "multi_factor_authentication",
            "vpn_connection",
            "vpn_disconnection",
            "email_sent",
            "email_received",
            "print_job_started",
            "print_job_completed"
        ]
        event_type = random.choice(event_types)
        active_hours = "8:00-17:00"

        # Filters users and servers to be used in the event
        users = self.data_manager.read_doc("users", users_query)
        servers = self.data_manager.read_doc("servers", servers_query)

        # Validates that there are users or servers available.
        if not users or not servers:
            self.logger.warning("No users or servers available for event generation.")
            return

        # Pick a random user and server.
        user = random.choice(list(users))
        server = random.choice(list(servers))

        # Verify the user is in active hours (NOT implemented/in use yet)
        if not self.is_user_active(user, active_hours):
            self.logger.warning("User not active.")
            return None

        # Generates event
        # Generic format for now, it can be improved or have a more custom solution
        event = {
            "timestamp": time.time(),
            "user": user["username"],
            "server": server["server_name"],
            "action": event_type,
            "details": {
                "user_role": user["role"],
                "user_ip": user.get("ip_address", "unknown"),
                "server_role": server["server_type"],
                "server_ip": server.get("ip_address", "unknown")
            }
        }
        self.logger.info("Generated event.")
        self.logger.debug(f"Generated event: {event}")
        return event

    def is_user_active(self, user, active_hours):
        return True
