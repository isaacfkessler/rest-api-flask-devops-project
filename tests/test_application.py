import pytest
from application import create_app

class TestApplication():

    @pytest.fixture
    def client():
        app = create_app('config.MockConfig')
        yield app.test_client()