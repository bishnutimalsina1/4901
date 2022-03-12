import pytest

from __init__ import db, flask_bcrypt
from models import UserInfo, BusinessType
import app


@pytest.fixture
def flask_app():
    # Setup app for testing
    flask_app = app.app

    flask_app.config['TESTING'] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.testing = True

    with flask_app.app_context():
        db.create_all()
        passwd = flask_bcrypt.generate_password_hash("test")

        user1 = UserInfo(first_name="foo",
                         last_name="bar",
                         email="test@email.com",
                         password=passwd,
                         business=None,
                         business_type=None
                         )
        db.session.add(user1)
        business_type = BusinessType(title="lorem", description="ipsum")
        db.session.add(business_type)
        db.session.commit()
    yield flask_app


@pytest.fixture
def client(flask_app):
    client = flask_app.test_client()
    return client


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@email.com", password="test"):
        return self._client.post(
            "/login",
            data={"email": email, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)