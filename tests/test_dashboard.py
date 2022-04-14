import pytest


@pytest.mark.usefixtures('logged_in_user')
def test_dashboard(client):
    resp = client.get('/dashboard')
    assert resp.status_code == 200


