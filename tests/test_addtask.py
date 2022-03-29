import pytest
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_add_task(client):
    resp = client.post('/addTask', json={
        'job_title': 'task_name',
        'job_description': "",
        'job_hourly_pay': '10',
        'business_id': 'user_id',
        'user_id': 'user_id',
        'job_required_skills': "",
        'is_active': 'T',
        'is_complete': 'F',
        'job_started_on': 'start',
        'job_complete_on': 'end', 'progress': '23', 'color': 'blue'
    })
    assert resp.status_code == 200
    assert resp.json.get('success')


def test_add_task_bad_http_method(client):
    resp = client.get('/addTask')
    assert resp.status_code == 405


def test_add_task_no_json_body(client):
    resp = client.post('/addTask', data='something')
    assert resp.status_code == 400
    assert not resp.json.get('success')


def test_add_task_missing_task_name(client):
    resp = client.post('/addTask', json={'username': 'mehdi'})
    assert resp.status_code == 400
    assert not resp.json.get('success')
