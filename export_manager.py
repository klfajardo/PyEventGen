import json
import logging
# import csv <- to be implemented
# import xml <- to be implemented
from datetime import datetime

# TODO: Implement XML, CSV, and see which other formats could be useful
# TODO: Study more these libraries

class ExportManager():
    def __init__(self):
        self.export_strategies = {
            "csv": self.export_to_csv,
            "json": self.export_to_json,
            "xml": self.export_to_xml,
            "log": self.export_to_log,
            "none": self.export_to_none
        }
        self.logger = logging.getLogger("ExportManager")
        self.logger.info("ExportManager component initialized.")

    def verify_export_format(self, format):
        """
        Verifies that the format is valid.
        :param format: [String] Format to be used.
        :return: Boolean
        """

        if format.strip() not in self.export_strategies:
            self.logger.error(f"Unsupported format: {format}")
            return False
        self.logger.info(f"Verified format successfully: {format}")
        return True

    def export(self, events, format):
        """
        Export a list of events in the given format.
        Selects the correct function from 'export_strategies' for
        the given format
        :param events: [List] The events to be exported.
        :param format: [String] The format to export the events
        """

        if not self.verify_export_format(format):
            return
        self.export_strategies[format](events)
        # Crazy line of code here
        # It replaces the line with the needed function from 'export_strategies'

    def export_to_none(self, events):
        """
        Receives events but doesn't export them. Useful for testing.
        :param events: [List] Events to be exported
        """
        print("The export format is 'none' so nothing is exported, the events are only printed.")
        self.logger.info(f"{(len(list(events)))} events were provided but not exported. Format = 'none'.")

    def export_to_json(self, events):
        """
        Exports list of events to a file in JSON format
        :param events: [List] Events to be exported
        """

        # Opens a file 'filename' with Write permission
        # If file already exists, overwrites the content
        # If file doesn't exist, creates a new one
        filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as file:
            json.dump(events, file, indent=4)
        print(f"Events exported to {filename}")
        self.logger.info(f"{(len(list(events)))} events exported to {filename} in JSON format.")

    def export_to_log(self, events):
        """
        Exports list of events to a file in log format
        :param events: [List] Events to be exported
        """

        # Opens a file 'filename' with Write permission
        # If file already exists, overwrites the content
        # If file doesn't exist, creates a new one
        filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(filename, "w") as file:
            for event in events:
                file.write(f"{datetime.now()} - {json.dumps(event)}\n")
            print(f"Events exported to {filename}")
            self.logger.info(f"{(len(list(events)))} events exported to {filename} in LOG format.")

    # TODO:
    def export_to_csv(self, events):
        print("Export to CSV: To be implemented... soon")
    def export_to_xml(self, events):
        print("Export to XML: To be implemented... soon")
      
