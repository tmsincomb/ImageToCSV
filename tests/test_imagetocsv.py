#!/usr/bin/env python

"""Tests for `imagetocsv` package."""
from imagetocsv import imagetocsv


def test_imagetocsv(fixture_setup):
    no_grid_path = fixture_setup.get_no_grid()
    df = imagetocsv(no_grid_path)
    csv = df.to_csv(index=False, header=False).strip()
    csv = "\n".join(csv.splitlines()).strip()
    csv = [line.strip().split(",") for line in csv.splitlines()]
    with open(fixture_setup.base_datadir / "no-grid.csv", "r") as f:
        assert csv == [line.strip().split(",") for line in f.read().strip().split("\n")]


def test_imagetocsv_with_label_and_index(fixture_setup):
    no_grid_path = fixture_setup.get_no_grid()
    df = imagetocsv(
        no_grid_path,
        index_name="Population",
        index=[
            "All Events",
            "Lymphocytes",
            "Single cells...",
            "Single cells...",
            "Live/Dead",
            "CD19+ Dump-",
            "Naive gD+",
            "Memory IgD-",
            "IgD- KO-",
            "P15-1",
            "P15-2",
            "P15-3",
            "P15-4",
            "MARIO WT++",
            "P14-1",
            "P14-2",
            "P14-3",
            "P14-4",
        ],
        column_header=["Events", "%Parent", "%Total", "FSC-A Median", "FSC-A %rCV", "SSC-A Median", "SSC-A %rCV"],
    )
    csv = df.to_csv(index=False, header=False).strip()
    csv = "\n".join(csv.splitlines())
    csv = [line.strip().split(",") for line in csv.splitlines()]
    with open(fixture_setup.base_datadir / "no-grid-index-label.csv", "r") as f:
        assert csv == [line.strip().split(",") for line in f.read().strip().split("\n")]
