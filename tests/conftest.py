import re

import pytest

from __init__ import db, flask_bcrypt
from app import login_manager
from models import UserInfo, BusinessType, UserProfile, Business
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
        db.session.commit()

        

        passwd = flask_bcrypt.generate_password_hash("test").decode('utf-8')
        business_type = BusinessType(title="lorem", description="ipsum")
        db.session.add(business_type)
        db.session.commit()

        business = Business(
            business_name="test",
            phone="1234567890",
            email="a@e.c",
            description="lorem ipsum",
            business_type=1,
        )
        db.session.add(business)
        db.session.commit()

        user1 = UserInfo(first_name="foo",
                         last_name="bar",
                         email="test@email.com",
                         password=passwd,
                         business=1,
                         business_type=1
                         )
        db.session.add(user1)
        db.session.commit()

        user_profile = UserProfile(
            user_id=1,
            business=1,
            user_description="",
            salary="",
            pay_frequency="",
            experience_years="",
            employment_type="",
            phone="",
            city="",
            state="",
            twitter_link="",
            facebook_link="",
            website_link="",
            skills_description="",
        )
        db.session.add(user_profile)
        db.session.commit()

    yield flask_app


@pytest.fixture
def client(flask_app):
    client = flask_app.test_client()
    return client


@pytest.fixture
def logged_in_user(client):
    @login_manager.request_loader
    def load_user_from_request(request):
        return UserInfo.query.first()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="test@email.com", password="test"):
        response = self._client.get("/login")
        csrf_token = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">',
                               response.data).group(1).decode('utf-8')
        return self._client.post(
            "/login",
            data={"email": email, "password": password, "csrf_token": csrf_token},
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
