import pytest
from application import create_app
import datetime


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()
    
    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Isaac",
            "last_name": "Caasi",
            "cpf": "446.231.940-00",
            "email": "isaac@gmail.com",
            "birth_date": "1953-03-29"
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Isaac",
            "last_name": "Caasi",
            "cpf": "446.231.940-01",
            "email": "isaac@gmail.com",
            "birth_date": "1953-03-29"
        }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"sucessfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"CPF is invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get('/user/%s' % valid_user["cpf"])

        user_data = response.json[0]
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "Isaac"
        assert response.json[0]["last_name"] == "Caasi"
        assert response.json[0]["cpf"] == "446.231.940-00"
        assert response.json[0]["email"] == "isaac@gmail.com"
        birth_date_timestamp = user_data["birth_date"]["$date"]["$numberLong"]
        birth_date = datetime.datetime.utcfromtimestamp(int(birth_date_timestamp) / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
        assert birth_date == "1953-03-29T00:00:00Z"

        response = client.get('/user/%s' % invalid_user["cpf"])
        assert response.status_code == 400
        assert b"User does not exist in database" in response.data


    def test_patch_user(self, client, valid_user):
        valid_user["first_name"] = "Isaac"
        response = client.patch('/user', json=valid_user)
        assert response.status_code == 200
        assert b"updated" in response.data

        valid_user["cpf"] = "199.624.120-64"
        response = client.patch('/user', json=valid_user)
        assert response.status_code == 400
        assert b"does not exist in database" in response.data