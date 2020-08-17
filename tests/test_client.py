from vantage6.client import Client
from unittest.mock import patch, MagicMock

# Mock server
HOST = 'mock_server'
PORT = 1234

# Mock credentials
USERNAME = 'vantage6_test'
PASSWORD = 'secretpassword'
FAKE_ID = 1

TASK_NAME = 'test-task'
TASK_IMAGE = 'mock-image'
COLLABORATION_ID = 1
ORGANIZATION_IDS = [1]


def test_post_task():
    mock_jwt = MagicMock()
    mock_jwt.decode.return_value = {'identity': FAKE_ID}

    mock_requests = MagicMock()
    mock_requests.get.return_value.status_code = 200
    mock_requests.post.return_value.status_code = 200

    input_ = {'method': TASK_NAME}

    with patch.multiple('vantage6.client', requests=mock_requests, jwt=mock_jwt):
        client = Client(HOST, PORT)
        client.authenticate(USERNAME, PASSWORD)
        client.setup_encryption(None, disabled=True)

        client.post_task(name=TASK_NAME, image=TASK_IMAGE, collaboration_id=COLLABORATION_ID,
                         organization_ids=ORGANIZATION_IDS, input_=input_)
        pass
