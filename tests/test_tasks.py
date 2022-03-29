import re

import pytest
from models import UserInfo, Jobs, Projects


@pytest.mark.usefixtures('logged_in_user')
def test_add_task(client, flask_app):
    """
    GIVEN a Flask application
    WHEN the '/test_add_task' page is requested (Post)
    THEN check the response is valid
    """

    # Ensure that the user is logged in
    response = client.get('/dashboard')
    assert response.status_code == 200

    task_data = {
        'task_name': 'foo',
        'eventstarttime': '00:00',
        'eventstartdate': '2022-02-22',
        'eventendtime': '00:00',
        'eventenddate': "2022-05-05",
        'progress': 1,
        'exampleColorInput': 'blue',
        'user_id': 1
    }
    response = client.post(
        '/addTask',
        data=task_data,
    )
    # Check the response is valid and redirects to the dashboard
    assert response.headers['Location'] == 'http://localhost/dashboard'
    # test if user is registered and exists
    with flask_app.app_context():
        job = Jobs.query.first()
        assert job is not None
        assert job.job_title == task_data['task_name']
        assert job.progress == task_data['progress']
        assert job.user_id == task_data['user_id']
        assert job.color == task_data['exampleColorInput']
