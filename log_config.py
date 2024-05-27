import logging
# import logging.config

def setup_logging(log_file="pyeventgen.log"):
    """
    Sets the logging configuration for the PyEventGen app.
    The logs are saved in 'pyeventgen.log' in the installation directory.
    :param log_file: Filepath where the internal messages are being logged.
    :return:
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            #logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('log_config')
    logger.info("Logging configuration initialized.")

# Initialize logger (Not in use, now being called from __init__ from command_line.py)
# This will be removed
setup_logging()
# logger = logging.getLogger('PyEventGen')
# logger.info("Logging configuration initialized.")
