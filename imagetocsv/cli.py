"""Console script for imagetocsv."""
from __future__ import annotations

import sys
from pathlib import Path

import click

from imagetocsv import imagetocsv

from .hardcoded_options import options


@click.command()
@click.version_option()
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Vebosity level, ex. -vvvvv for debug level logging",
)
@click.option(
    "--index_name",
    "-n",
    type=click.STRING,
    default=None,
    help="Index Name for the CSV file",
)
@click.option(
    "--index",
    "-i",
    type=click.STRING,
    default=None,
    help="Index for the CSV file",
)
@click.option(
    "--column_header",
    "-c",
    type=click.STRING,
    default=None,
    help="Columns for the CSV file",
)
@click.option(
    "--preconfigured-options",
    "-p",
    type=click.STRING,
    default=None,
    help="Preconfigured Index/Header Options",
)
@click.argument(
    "image_path",
    required=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
@click.argument(
    "csv_path",
    required=False,
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
def main(
    verbose: bool,
    index_name: str,
    index: str,
    column_header: str,
    preconfigured_options: str,
    image_path: str,
    csv_path: str,
):
    """Console script for imagetocsv."""
    if preconfigured_options:
        try:
            index_name, index, column_header = options[preconfigured_options]
        except KeyError:
            raise KeyError(
                f"preconfigured_options {preconfigured_options} not found, following options are available: {options}"
            )

    if Path(image_path).exists() is False:
        raise FileNotFoundError(f"File {image_path} does not exist")

    df = imagetocsv(image_path, index_name, index, column_header)

    if csv_path and Path(csv_path).name != "-":
        df.to_csv(csv_path, index=index, header=column_header)
    else:
        print(df.to_csv(index=index, header=column_header))


if __name__ == "__main__":
    # print("Running imagetocsv.cli.main()")
    sys.exit(main())  # pragma: no cover
