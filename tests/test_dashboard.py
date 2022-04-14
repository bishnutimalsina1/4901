import pytest


@pytest.mark.usefixtures('logged_in_user')
def test_dashboard(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 200


def test_dashboard_bad_http_method(client):
    resp = client.post('/dashboard')
    assert resp.status_code == 405


def test_dashboard_401_http_method(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 401
