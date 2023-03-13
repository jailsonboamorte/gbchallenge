import pathlib

import pytest


@pytest.fixture
def base_dir():
    """
    The base project directory
    """
    root_project_dir = pathlib.Path(__file__).parents[2]  # Up two levels
    source_dir = root_project_dir
    return str(source_dir)
