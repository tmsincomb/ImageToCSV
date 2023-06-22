"""Console script for imagetocsv."""
from __future__ import annotations

import sys
from pathlib import Path

import click

from imagetocsv import imagetocsv

from .hardcoded_options import options


@click.command()
@click.version_option()
# @click.option(
#     "--verbose",
#     "-v",
#     is_flag=True,
#     help="Vebosity level, ex. -vvvvv for debug level logging",
# )
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
    "--columns",
    "-c",
    type=click.STRING,
    default=None,
    help="Columns for the CSV file",
)
@click.option(
    "--preconfigured-option",
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
    index_name: str,
    index: list[str],
    columns: list[str],
    preconfigured_option: str,
    image_path: str,
    csv_path: str,
) -> None:
    """Console script for imagetocsv.

    Parameters
    ----------
    verbose : bool
        Vebosity level, ex. -vvvvv for debug level logging
    index_name : str
        Index Name for the CSV file
    index : list[str]
        Index for the CSV file
    columns : list[str]
        Columns for the CSV file
    preconfigured_option : str
        Preconfigured Index/Header Options
    image_path : str
        Path for input image
    csv_path : str
        Path for output CSV file

    Raises
    ------
    KeyError
        Preconfigured Option not found
    FileNotFoundError
        Input Image not found
    """
    if preconfigured_option:
        try:
            index_name, index, columns = options[preconfigured_option]
        except KeyError:
            raise KeyError(
                f"preconfigured_option {preconfigured_option} not found, following options are available: {options.keys()}"
            )

    if Path(image_path).exists() is False:
        raise FileNotFoundError(f"File {image_path} does not exist")

    df = imagetocsv(image_path, index_name, index, columns)
    show_index = True if index else False

    if csv_path and Path(csv_path).name != "-":
        df.to_csv(path_or_buf=csv_path, index=show_index, header=columns)
    else:
        print(df.to_csv(index=show_index, header=columns), file=sys.stdout)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
