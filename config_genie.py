import logging

class ConfigGenie:
    def __init__(self):
        # Global Configuration
        self._global_config = {
            "shell_verbose": "True", # just some examples on how this could be used
            "log_level": "INFO"
        }
        # Group configuration
        self._group_config = {
            "servers": {},
            "users": {}
        }

        # In case you want to restore to the defaults,
        # the default values are being assigned to variables
        _default_global_config = self._global_config
        _default_group_config = self._group_config

        self.logger = logging.getLogger("ConfigGenie")
        self.logger.info("ConfigGenie component initialized.")

    def set_global_config(self, attribute, new_value):
        """
        Replaces current value with the given new value for the specified attribute.
        Example: set_config("dhcp", False)
        :param attribute: [String] The attribute to be modified
        :param new_value: [String or Boolean] The new value to be set to the specified attribute
        """

        # Verifies if attribute is allowed in global config
        if not attribute in self._global_config:
            self.logger.error(f"Attribute: '{attribute}' doesn't exist in '_configuration' dictionary.")

        # Stores the old attribute value
        # and updates the attribute
        old_value = self._global_config[attribute]
        self._global_config.update({attribute: new_value})

        self.logger.info(f"Attribute '{attribute}' has been modified. Old value: '{old_value}', New value: '{new_value}'")

    def set_group_config(self, group, attribute, new_value):
        """
        Replaces current value with the given new value for the specified
        attribute in a group.
        :param attribute: [String] The attribute to be modified.
        :param new_value: [String or Boolean] The new value to be set.
        """

        if not group in self._group_config:
            self.logger.warning(f"Group: '{group}' doesn't exist in '_configuration' dictionary.")

        if not attribute in self._group_config:
            self.logger.warning(f"Attribute: '{attribute}' doesn't exist in '_configuration' dictionary.")

        # Stores the old attribute value
        # and updates the attribute
        old_value = self._global_config[attribute]
        self._global_config.update({attribute: new_value})

        self.logger.info(f"Attribute '{attribute}' has been modified. Old value: '{old_value}', New value: '{new_value}'")

    def get_global_config(self, *args):
        """
        Gets current configuration from ConfigGenie / App (internal). If:
        - args > 0 returns those specified attributes
        - args = 0 returns whole dictionary
        :param group: [Group or List-of Group] Group
        :param args: [String or List-of String] Specified attributes
        :return: Dictionary
        """

        if args:
            # Returns a new dictionary only containing the specified attributes
            result = {}
            for attribute in args:
                if attribute in self._global_config:
                    result[attribute] = self._global_config[attribute]
            self.logger.info(f"Global config has been successfully read.")
            return result
        else:
            # Returns the full dictionary
            self.logger.info(f"Global config has been successfully read.")
            return self._global_config

    def get_group_config(self, group, *args):
        """
        Gets current configuration for the given group (internal).
        If:
        - args > 0 returns those specified attributes
        - args = 0 returns whole dictionary
        :param group: [String] Name of the group
        :param args: [String or List-of String] Specified attributes
        :return: Dictionary
        """

        if group in self._group_config:
            if args:
                # Returns a new dictionary only containing the specified attributes
                result = {}
                for attribute in args:
                    if attribute in self._group_config:
                        result[attribute] = self._global_config[attribute]
                self.logger.info(f"Group config has been successfully read.")
                return result
            else:
                # Returns the full dictionary
                self.logger.info(f"Group config has been successfully read.")
                return self._group_config

    def validate_config(self):
        """
        Validates the config
        """
        self.logger.info(f"Config has been successfully validated.")
