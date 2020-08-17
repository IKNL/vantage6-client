from vantage6.client import Client
from unittest.mock import patch, MagicMock
import base64
import pickle
import io

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


def test_post_task_legacy_method():
    input_ = {'method': TASK_NAME}

    decoded_input = post_task_on_mock_client(input_)

    assert {'method': TASK_NAME} == decoded_input


def post_task_on_mock_client(input_):
    mock_jwt = MagicMock()
    mock_jwt.decode.return_value = {'identity': FAKE_ID}
    mock_requests = MagicMock()
    mock_requests.get.return_value.status_code = 200
    mock_requests.post.return_value.status_code = 200
    with patch.multiple('vantage6.client', requests=mock_requests, jwt=mock_jwt):
        client = Client(HOST, PORT)
        client.authenticate(USERNAME, PASSWORD)
        client.setup_encryption(None)

        client.post_task(name=TASK_NAME, image=TASK_IMAGE, collaboration_id=COLLABORATION_ID,
                         organization_ids=ORGANIZATION_IDS, input_=input_)

        # In a request.post call, json is provided with the keyword argument 'json'
        # call_args provides a tuple with positional arguments followed by a dict with positional arguments
        post_content = mock_requests.post.call_args[1]['json']

        post_input = post_content['organizations'][0]['input']

        decoded_input = base64.b64decode(post_input)
        decoded_input = pickle.loads(decoded_input)
    return decoded_input


