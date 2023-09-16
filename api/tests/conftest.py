import pytest
from flaskr.app import create_app


@pytest.fixture(scope="module")
def app():
    """Instance of Flask APP"""
    return create_app()
