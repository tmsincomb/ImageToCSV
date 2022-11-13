#!/usr/bin/env python

"""Tests for `imagetocsv` package."""
import pandas as pd

from imagetocsv import imagetocsv


def test_imagetocsv(fixture_setup):
    no_grid_path = fixture_setup.get_no_grid()
    df = imagetocsv(no_grid_path)
    test_csv = df.to_csv(index=False, header=False, encoding="utf-8-sig")
    ref_csv = pd.read_csv(
        fixture_setup.base_datadir / "no-grid.csv", encoding="utf-8-sig", header=None, dtype=str
    ).to_csv(index=False, header=False, encoding="utf-8-sig")
    print(test_csv)
    print(ref_csv)
    assert test_csv == ref_csv


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
    test_csv = df.to_csv(encoding="utf-8-sig")
    ref_csv = pd.read_csv(
        fixture_setup.base_datadir / "no-grid-index-label.csv", encoding="utf-8-sig", header=None, dtype=str
    ).to_csv(index=False, header=False, encoding="utf-8-sig")
    print(test_csv)
    print(ref_csv)
    assert test_csv == ref_csv
