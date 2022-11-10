#!/usr/bin/env python

"""Tests for `imagetocsv` package."""
from pathlib import Path

import pytest
from click.testing import CliRunner

from imagetocsv import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface(fixture_setup):
    """Test the CLI."""
    runner = CliRunner()
    no_grid_path = fixture_setup.get_no_grid()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2
    assert "--help" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help" in help_result.output
    csv = runner.invoke(
        cli.main,
        [
            no_grid_path,
            "-",
        ],
    )
    with open(fixture_setup.base_datadir / "no-grid.csv", "r") as f:
        assert csv.stdout.strip() == f.read().strip()
    csv = runner.invoke(
        cli.main,
        [
            no_grid_path,
            "-",
            "-p",
            "bib",
        ],
    )
    with open(fixture_setup.base_datadir / "no-grid-index-label.csv", "r") as f:
        assert csv.stdout.strip() == f.read().strip()
    csv = runner.invoke(
        cli.main,
        [
            no_grid_path,
            "-",
            "-n",
            "Population",
            "-i",
            "All Events,Lymphocytes,Single cells...,Single cells...,Live/Dead,CD19+ Dump-,Naive gD+,Memory IgD-,IgD- KO-,P15-1,P15-2,P15-3,P15-4,MARIO WT++,P14-1,P14-2,P14-3,P14-4",
            "-c",
            r"Events,%Parent,%Total,FSC-A Median,FSC-A %rCV,SSC-A Median,SSC-A %rCV",
        ],
    )
    with open(fixture_setup.base_datadir / "no-grid-index-label.csv", "r") as f:
        assert csv.stdout.strip() == f.read().strip()
