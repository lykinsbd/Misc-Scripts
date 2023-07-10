"""Tiller related CLI commands."""
import csv
import datetime
import logging
from pathlib import Path

import click
from dateutil import parser
from dateutil.relativedelta import relativedelta, SU
import rich

log = logging.getLogger(__name__)


@click.group()
@click.pass_context
def tiller(context: click.Context):  # pylint: disable=unused-argument
    """Group for all `tiller` related commands."""


@click.command()
@click.pass_context
@click.option("--account_name", type=click.STRING)
@click.option("--account_number", type=click.STRING)
@click.option("--csv_out", type=click.Path())
@click.argument("csv_in", type=click.Path(exists=True, readable=True, path_type=Path))
def modify(context: click.Context, account_name, account_number, csv_out, csv_in: Path) -> None:
    """Modify a given CSV to be in the format expected by Tiller.

    Returns: Dict with the modified contents to be written or used elsewhere.

    Args:
        context (click.Context): _description_
        account_name (_type_): _description_
        account_number (_type_): _description_
        csv_in (Path): _description_

    Raises:
        IOError: If the input CSV can't be parsed, raise IOError.

    Returns:
        None: Nothing.
    """

    tiller_headers = [
        "Date",
        "Description",
        "Category",
        "Amount",
        "Account",
        "Account #",
        "Institution",
        "Month",
        "Week",
        "Check Number",
        "Full Description",
        "Date Added",
    ]

    usaa_headers = [
        "Date",
        "Description",
        "Original Description",
        "Category",
        "Amount",
        "Status",
    ]

    usaa_csv = csv.reader(csv_in.open())

    # Validate the USAA Headers
    if next(usaa_csv) != usaa_headers:
        raise IOError(f"input CSV is not in known format, headers do not match: {usaa_headers}")

    # New CSV creation
    log.info("Beginning new CSV data creation.")
    tiller_csv = []
    time_format = "%-m/%-d/%y"
    for row in usaa_csv:
        tiller_csv_entry = {header: "" for header in tiller_headers}
        transaction_date = parser.parse(row[0])
        for header in tiller_headers:
            match header:
                case "Date":
                    tiller_csv_entry[header] = transaction_date.strftime(time_format)
                case "Description":
                    tiller_csv_entry[header] = row[1]
                case "Category":
                    tiller_csv_entry[header] = row[3]
                case "Amount":
                    tiller_csv_entry[header] = row[4]
                case "Account":
                    tiller_csv_entry[header] = account_name
                case "Account #":
                    tiller_csv_entry[header] = account_number
                case "Institution":
                    tiller_csv_entry[header] = "USAA"
                case "Month":
                    tiller_csv_entry[header] = (transaction_date + relativedelta(day=1)).strftime(time_format)
                case "Week":
                    tiller_csv_entry[header] = (transaction_date + relativedelta(weekday=SU(-1))).strftime(time_format)
                case "Full Description":
                    tiller_csv_entry[header] = row[2]
                case "Date Added":
                    tiller_csv_entry[header] = datetime.datetime.now().strftime(time_format)
        tiller_csv.append(tiller_csv_entry)

    # rich.print(tiller_csv)
    log.debug("Created the following csv: %s", tiller_csv)

    # Prepare to output the curated data
    if csv_out is None:
        csv_out = Path(f"{csv_in.parent}/tiller_{csv_in.name}")

    log.info("Writing new CSV to %s", csv_out)
    writer = csv.DictWriter(csv_out.open(mode="w", encoding="utf8"), fieldnames=tiller_headers)
    writer.writeheader()
    for row in tiller_csv:
        writer.writerow(row)


tiller.add_command(modify)
