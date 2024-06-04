import json
import logging
import csv
import xml.etree.ElementTree as ET

from datetime import datetime
from colors import Colors


class ExportManager:

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

    def verify_export_format(self, format_str):
        """
        Verifies that the format is valid.
        :param format_str: [String] Format to be used.
        :return: Boolean
        """

        if format_str.strip() not in self.export_strategies:
            message = f"Unsupported format: {format_str}"
            self.logger.error(message)
            print(f"{Colors.FAIL}{message}{Colors.ENDC}")
            return False
        self.logger.info(f"Verified format successfully: {format_str}")
        return True

    def export(self, events, format_str):
        """
        Export a list of events in the given format.
        Selects the correct function from 'export_strategies' for
        the given format
        :param events: [List] The events to be exported.
        :param format_str: [String] The format to export the events
        """

        if not self.verify_export_format(format_str):
            return
        self.export_strategies[format_str](events)
        # Crazy line of code here
        # It replaces the line with the needed function from 'export_strategies'

    def export_to_none(self, events):
        """
        Receives events but doesn't export them. Useful for testing.
        :param events: [List] Events to be exported
        """

        message = f"The export format is 'none' so nothing was exported."
        print(f"{Colors.OKGREEN}{message}{Colors.ENDC}")
        self.logger.info(f"{(len(list(events)))} events were provided. {message}")

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

        message = f"Events exported to {filename}"
        print(f"{Colors.OKGREEN}{message}{Colors.ENDC}")
        self.logger.info(f"{(len(list(events)))} {message.lower()}")

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

        message = f"Events exported to {filename}"
        print(f"{Colors.OKGREEN}{message}{Colors.ENDC}")
        self.logger.info(f"{(len(list(events)))} {message.lower()}")

    def export_to_csv(self, events):
        """
        Exports list of events to a file in csv format
        :param events: [List] Events to be exported
        """

        # If file doesn't exist, it creates a new one
        filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Write header based on event keys
            if events:
                header = events[0].keys()
                writer.writerow(header)
                for event in events:
                    writer.writerow(event.values())

        message = f"Events exported to {filename}"
        print(f"{Colors.OKGREEN}{message}{Colors.ENDC}")
        self.logger.info(f"{(len(list(events)))} {message.lower()}")

    def export_to_xml(self, events):
        """
        Exports list of events to a file in xml format
        :param events: [List] Events to be exported
        """

        # If file doesn't exist, it creates a new one
        filename = f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

        root = ET.Element("Events")
        for event in events:
            event_element = ET.Element("Event")
            for key, value in event.items():
                child = ET.SubElement(event_element, key)
                child.text = str(value)
            root.append(event_element)

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

        message = f"Events exported to {filename}"
        print(f"{Colors.OKGREEN}{message}{Colors.ENDC}")
        self.logger.info(f"{(len(list(events)))} {message.lower()}")
