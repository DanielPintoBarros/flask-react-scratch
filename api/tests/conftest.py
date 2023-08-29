import pytest
from flaskr.app import create_app


@pytest.fixture(scope="module")
def app():
    """Instance of Mais Flask APP"""
    return create_app()
