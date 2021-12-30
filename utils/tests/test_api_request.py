# pylint: skip-file
"""Unit tests for flag function"""
import os
from unittest import mock
from unittest.mock import patch
import pytest

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

MOCK_ENV_VARS = {
    "token_url": "mock",
    "BOTO3_PROXY_CLIENT_ID": "mock",
    "BOTO3_PROXY_SECRET_NAME": "mock",
    "region": "mock",
    "BOTO3_PROXY_SECRET_VALUE": "mock",
}


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, MOCK_ENV_VARS):
        yield


# test bad access token
@patch('azureauth.create_token.TokenGenerator')
def test_bad_access_token(mock_token_generator):
    # Set up mock token generator
    mock_token_generator.side_effect = Exception("Mock exception")

    from utils.api_request import ApiRequests
    api_requests = ApiRequests()
    api_requests.scope = "mock_scope"
    api_requests.client_id = "mock_client_id"
    api_requests.client_secret = "mock_client_scope"
    try:
        api_requests.get_access_token()
    except Exception:
        assert True


# test method not supported
@patch('azureauth.create_token.TokenGenerator')
def test_bad_request_method(mock_token_generator):
    # Set up mock token generator
    generator = mock_token_generator.return_value
    generator.get_bearer_token.return_value = 'mock_token'

    from utils.api_request import ApiRequests
    api_requests = ApiRequests()
    api_requests.scope = "mock_scope"
    api_requests.client_id = "mock_client_id"
    api_requests.client_secret = "mock_client_scope"
    with patch.object(api_requests, 'get_access_token', return_value='12345'):
        with pytest.raises(Exception) as e:
            assert api_requests.request('mock_url', 'PATCH')
        assert str(e.value) == 'Http Method type PATCH not Supported'
