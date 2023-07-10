"""
Logging utilities for CSVIFY CLI.

This module contains helpers and wrappers for making logging more consistent across applications.

How to use me:

    >>> from csvify.log import initialize_logging
    >>> log = initialize_logging(level="debug")
    2021-12-07T10:51:49-0700 [DEBUG] [log] [initialize_logging] csvify: Logging initialized.
    >>> log.info("NTC")
    2021-12-07T10:51:49-0700 [INFO] [cli] [main] csvify.cli: Entrypoint of the CLI app.
"""
import logging.config

APP = "csvify"


def initialize_logging(config=None, level="INFO", filename=None, rich_logging=False):
    """Initialize logging using sensible defaults.

    Args:
        config (dict): User provided configuration dictionary.
        level (str): The level of logging for STDOUT logging.
        filename (str): Where to output debug logging to file.
        rich_logging (bool): Enable "rich" formatted logging.

    """
    if not config:
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
                "debug": {
                    "format": "%(asctime)s [%(levelname)s] [%(module)s] [%(funcName)s] %(name)s: %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "standard": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": level.upper(),
                },
            },
            "loggers": {
                "": {
                    "handlers": ["standard"],
                    "level": "DEBUG",
                }
            },
        }

        # If a filename is passed in, let's add a FileHandler
        if filename:
            config["handlers"].update(
                {
                    "file_output": {
                        "class": "logging.FileHandler",
                        "formatter": "debug",
                        "level": "DEBUG",
                        "filename": filename,
                    }
                }
            )
            config["loggers"][""]["handlers"].append("file_output")

        # If rich logging is requested, modify the standard handler
        if rich_logging:
            config["formatters"]["standard"]["format"] = "%(message)s"
            config["formatters"]["debug"]["format"] = "%(message)s"
            config["handlers"]["standard"]["class"] = "rich.logging.RichHandler"
            config["handlers"]["standard"]["omit_repeated_times"] = False
            config["handlers"]["standard"]["rich_tracebacks"] = True

    # Configure the logging
    logging.config.dictConfig(config)

    # Initialize root logger and advise logging has been initialized
    log = logging.getLogger(APP)
    log.debug("Logging initialized.")
