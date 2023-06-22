from pathlib import Path

import pytest


class PathFixture:
    def __init__(self, tmp_path_factory: pytest.TempPathFactory) -> None:
        self.tmp_path = tmp_path_factory.mktemp("imagetocsv_fixture")
        self.base_datadir = Path("tests/data/")

    def get_no_grid(self) -> str:
        return str(self.base_datadir / "no-grid-index-label.jpg")


@pytest.fixture(scope="session", autouse=True)
def fixture_setup(tmp_path_factory: pytest.TempPathFactory) -> PathFixture:
    return PathFixture(tmp_path_factory)
