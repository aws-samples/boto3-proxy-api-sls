# pylint: skip-file
"""Unit tests for flag function"""
import os
from unittest import mock
from unittest.mock import patch
import pytest
import botocore
from utils.exceptions import InvalidRegionException

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

MOCK_ENV_VARS = {
    "LDAP_SERVER": "mock",
    "LDAP_USERNAME": "mock",
    "LDAP_PASSWORD_SECRET_NAME": "mock",
    "LDAP_SEARCH_BASE": "mock",
    "LDAP_OBJECT_CLASS": "mock",
    "LDAP_GROUP_NAME": "mock",
    "LDAP_LOOKUP_ATTRIBUTE": "mock",
    "MSFT_IDP_TENANT_ID": "mock",
    "MSFT_IDP_APP_ID": "mock",
    "MSFT_IDP_CLIENT_ROLES": "mock",
    "vpcxiam_endpoint": "mock",
    "vpcxiam_scope": "mock",
    "vpcxiam_host": "mock"
}


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, MOCK_ENV_VARS):
        yield


# test statusCode=401, unauthorized
@patch('utils.secrets.retrieve_ldap_password')
@patch('cloudx_sls_authorization.lambda_auth.authorize_lambda_request')
def test_handler_bad_auth(mock_auth, mock_ldap):
    """Raising 401 (Unauthorized) error when authentication token is invalid"""
    # Import
    from boto3_proxy import index

    # Mock ldap
    mock_ldap.return_value = "54321"
    # Setup mock failed auth
    mock_auth.side_effect = Exception("Mock exception")
    event = {"headers": [], "body": '{}'}

    # Call method
    result = index.handler(event, None)
    assert result['statusCode'] == 401
    assert result['body'] == "{\"error\": \"Unauthorized. Mock exception\"}"


# test statusCode=404, invalid account
@patch('utils.secrets.retrieve_ldap_password')
@patch('cloudx_sls_authorization.lambda_auth.authorize_lambda_request')
@patch('utils.api_request.ApiRequests')
def test_handler_invalid_account(mock_api_request, mock_auth, mock_ldap):
    """Raising 404 (Not Found) error when account not found"""
    # Import
    from boto3_proxy import index

    # Mock ldap and auth
    mock_ldap.return_value = "54321"
    mock_auth.return_value = True
    # Mock API request
    mock_api_request.return_value.request.return_value.text = '{\'error\':\'error\'}'

    event = {"headers": [], "body": '{}', "pathParameters": {"account-id": "111111111"}}

    # Call method
    result = index.handler(event, None)
    assert result['statusCode'] == 404


# test statusCode=400, service not supported
@patch('utils.secrets.retrieve_ldap_password')
@patch('cloudx_sls_authorization.lambda_auth.authorize_lambda_request')
@patch('utils.api_request.ApiRequests')
@patch('boto3.client')
def test_handler_invalid_service(mock_boto3_client, mock_api_request, mock_auth, mock_ldap):
    """Raising 400 (Bad Request) error when service not supported"""
    # Import
    from boto3_proxy import index

    # Mock ldap and auth
    mock_ldap.return_value = "54321"
    mock_auth.return_value = True
    # Mock API request
    mock_api_request.return_value.request.return_value.text = '{}'
    # Mock Boto3 client
    mock_client = mock_boto3_client.return_value

    # Mock get parameter call to throw an exception
    def get_parameter_side_effect(**kwargs):
        raise botocore.exceptions.ClientError({"Error": {"Code": "ParameterNotFound",
                                               "Message": "Parameter was not found"}}, 'get_parameter')
    mock_client.get_parameter.side_effect = get_parameter_side_effect

    event = {"headers": [], "body": '{}', "pathParameters": {"boto3-service": "invalid-service"}}

    # Call method
    result = index.handler(event, None)
    assert result['statusCode'] == 400
    assert result['body'] == "{\"error\": \"Service invalid-service is not an allowed service for the API\"}"


# test statusCode=400, action not supported
@patch('utils.secrets.retrieve_ldap_password')
@patch('cloudx_sls_authorization.lambda_auth.authorize_lambda_request')
@patch('utils.api_request.ApiRequests')
@patch('boto3.client')
def test_handler_invalid_action(mock_boto3_client, mock_api_request, mock_auth, mock_ldap):
    """Raising 400 (Bad Request) error when action not supported"""
    # Import
    from boto3_proxy import index

    # Mock ldap and auth
    mock_ldap.return_value = "54321"
    mock_auth.return_value = True
    # Mock API request
    mock_api_request.return_value.request.return_value.text = '{}'
    # Mock Boto3 client
    mock_client = mock_boto3_client.return_value
    mock_client.get_parameter.return_value = {'Parameter': {'Value': 'authorize_ingress,authorize_egress'}}

    event = {"headers": [], "body": '{}', "pathParameters": {"boto3-service": "ec2", "boto3-action": "invalid-action"}}

    # Call method
    result = index.handler(event, None)
    assert result['statusCode'] == 400
    assert result['body'] == "{\"error\": \"Action invalid-action is not an allowed action for the API\"}"


# test statusCode=404, invalid region
@patch('utils.secrets.retrieve_ldap_password')
@patch('cloudx_sls_authorization.lambda_auth.authorize_lambda_request')
@patch('utils.api_request.ApiRequests')
@patch('boto3.client')
@patch('utils.helpers')
def test_handler_invalid_region(mock_helper, mock_boto3_client, mock_api_request, mock_auth, mock_ldap):
    """Raising 404 (Not Found) error when region not found"""
    # Import
    from boto3_proxy import index

    # Mock ldap and auth
    mock_ldap.return_value = "54321"
    mock_auth.return_value = True
    # Mock API request
    mock_api_request.return_value.request.return_value.text = '{}'
    # Mock Boto3 client
    mock_client = mock_boto3_client.return_value
    mock_client.get_parameter.return_value = {'Parameter': {'Value': 'authorize_ingress,authorize_egress'}}

    event = {"headers": [], "body": '{}', "pathParameters": {
        "region-name": "invalid-region", "boto3-service": "ec2", "boto3-action": "authorize_ingress"}}

    # Mock the helper is_region_valid function
    # Mock get parameter call to throw an exception
    def is_region_valid_side_effect(**kwargs):
        raise InvalidRegionException

    mock_helper.is_region_valid.side_effect = is_region_valid_side_effect

    # Call method
    result = index.handler(event, None)
    assert result['statusCode'] == 404
    assert result['body'] == "{\"error\": \"Please enter a valid region in the url path\"}"
