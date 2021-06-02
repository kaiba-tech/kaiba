import json

import pytest


@pytest.fixture(scope='session')
def valid() -> dict:
    """Load a valid example config."""
    with open('tests/json/valid.json', 'r') as file_object:
        return json.loads(file_object.read())


@pytest.fixture(scope='session')
def invalid() -> dict:
    """Load an invalid example config."""
    with open('tests/json/invalid.json', 'r') as file_object:
        return json.loads(file_object.read())
