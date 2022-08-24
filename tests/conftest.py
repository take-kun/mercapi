import pytest
from vcr import VCR

from mercapi import mercapi


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "cassette_library_dir": "cassettes",
        "path_transformer": VCR.ensure_suffix(".yml"),
    }


@pytest.fixture(scope="function")
def m():
    return mercapi.Mercapi()
