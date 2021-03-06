import re

import pytest
from models import UserInfo


def test_register(client, flask_app):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/register')
    assert response.status_code == 200
    # Get csrf token from response
    csrf_token = re.search(b'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*)">',
                           response.data).group(1).decode('utf-8')
    register_data = {
        'first_name': 'foo',
        'last_name': 'bar',
        'email': 'test_2@email.com',
        'password': 'test12345',
        'business_name': "business_name",
        'business_type': 1,
        'csrf_token': csrf_token
    }
    response = client.post(
        '/register',
        data=register_data
    )
    # Check the response is valid and redirects to the dashboard
    assert response.headers['Location'] == 'http://localhost/'
    # test if user is registered and exists
    with flask_app.app_context():
        user = UserInfo.query.filter_by(email=register_data['email']).first()
        assert user is not None
        assert user.first_name == register_data['first_name']
        assert user.last_name == register_data['last_name']
        assert user.email == register_data['email']


def test_login(auth):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = auth.login()
    assert response.status_code == 200
    # Asset session cookie must be present
    assert response.headers.get("Set-Cookie") is not None
    assert "session" in response.headers.get("Set-Cookie")


@pytest.mark.usefixtures('logged_in_user')
def test_logout(auth):
    response = auth.logout()
    assert response.status_code == 302
    assert response.headers.get("Set-Cookie") is None
    assert response.headers['Location'] == 'http://localhost/'


def test_user_can_access_dashboard_after_login(client, auth):
    response = auth.login()
    assert response.status_code == 200
    response = client.get('/')
    assert response.status_code == 200


def test_user_cannot_access_dashboard_after_logout(client, auth):
    auth.logout()
    response = client.get('/dashboard')
    assert response.status_code == 401  # Unauthorized
