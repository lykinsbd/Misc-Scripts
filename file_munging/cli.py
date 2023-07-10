"""Mung files!"""
import logging
import logging.config

import click
from rich import traceback

from file_munging.config import load_or_exit
from file_munging.log import initialize_logging
from file_munging.tiller import tiller

APP = "csvify"

log: logging.Logger = logging.getLogger(__name__)

traceback.install(show_locals=True)


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Logging level",
)
@click.option(
    "--rich-logging",
    default=True,
    type=click.BOOL,
    help="Enable Rich log formatting, default True.",
)
@click.option("--log-file", default=None, help="Log file to output to debug logs to.")
@click.version_option()
@click.pass_context
def main(context: click.Context, log_level, rich_logging, log_file) -> None:  # pylint: disable=too-many-arguments
    """Entrypoint into `file-munging` app."""
    # Initialize the project
    settings = load_or_exit()
    initialize_logging(level=log_level, filename=log_file, rich_logging=rich_logging)
    log.info("Starting file-munging")

    # Ensure Context object exists and is a Dict
    context.ensure_object(dict)

    # Add project settings into the context
    context.obj["settings"] = settings

    # Setup environment variable prefix
    context.auto_envvar_prefix = "FILE_MUNGING"


main.add_command(tiller)
