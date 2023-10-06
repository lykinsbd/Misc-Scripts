"""Meal Plan updating CLI commands."""
import logging
from pathlib import Path
from string import digits

import click
import rich

log = logging.getLogger(__name__)


@click.group()
@click.pass_context
def meal_plan(context: click.Context):  # pylint: disable=unused-argument
    """Group for all `meal_plan` related commands."""


@click.command()
@click.pass_context
@click.argument("file_in", type=click.Path(exists=True, readable=True, path_type=Path))
def reorder(context: click.Context, file_in: Path) -> None:
    """Reorder the meal_plan doc so the newest is at top.

    Args:
        context (click.Context): _description_
        file_in (Path): _description_
    """

    input_lines: list[str] = file_in.read_text().splitlines()
    output_lines = []
    paragraph = []
    for line in input_lines:
        if line[-1:].isdigit():
            paragraph.insert(0, line)
        elif line != "":
            paragraph.append(line)
        else:
            paragraph.append("")
            output_lines = paragraph + output_lines
            paragraph.clear()

    rich.print("\n".join(output_lines))


meal_plan.add_command(reorder)
