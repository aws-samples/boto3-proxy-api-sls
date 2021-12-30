"""
contains behave step implementation
"""
# pylint: disable = import-error,no-name-in-module,line-too-long,C0111,W0603,W0613

import json

import requests
from hamcrest import assert_that, equal_to
import os
import sys
import time
from behave import then, given, when

THISDIR = os.path.dirname(__file__)  # steps/
TESTSDIR = os.path.dirname(THISDIR)  # bdd/

sys.path.insert(0, TESTSDIR)
sys.path.insert(0, THISDIR)

from tests import config, logger

DEFAULT_DELAY_SECONDS = 5


@given(u'the API POST /v1/accounts/<bdd_account>/regions/us-east-1/services/ec2/actions/authorize_security_group_ingress exists')
def step_impl(context):
    """
    Build the url with config items
    """
    account = config['main']['account']
    region = config['main']['region']
    vpce = config['behave']['vpc_endpoint']
    env = config['main']['environment']

    context.url = f'https://{vpce}/{env}/v1/accounts/{account}/regions/{region}' \
                  f'/services/ec2/actions/authorize_security_group_ingress'
    print(context.url)
    logger.info('--------------------------')
    logger.info(context.url)
    logger.info('--------------------------')


@given(u'valid oauth2 token for API authorization is generated')
def step_impl(context):
    """
    Get a valid token for the put storage tags API
    """
    logger.info("valid oauth2 token for API authorization is generated")
    context.token = context.api_client.get_access_token(context.application_scope)


@given(u'the VPCx account bdd_account is valid')
def step_impl(context):
    """
    Set the valid account from the config
    """
    account = config['main']['account']
    context.account = account


@when(u'we invoke the generic boto3 API with a valid request')
def step_impl(context):
    """
    Invoke the POST Boto3 Proxy API
    """
    logger.info("Invoking API")
    headers = {
        'authorization': context.token,
        'Host': context.api_host
    }
    kwargs = {
        'headers': headers
    }
    method = 'POST'

    # Create a valid request body with tags to query later
    context.from_port = 23
    context.to_port = 23
    context.cidr = '10.0.0.0/8'

    context.request_body = {'GroupId': context.security_group_id, 'IpPermissions': [{'IpProtocol': 'tcp',
                            'FromPort': context.from_port, 'ToPort': context.to_port, 'IpRanges': [{'CidrIp': context.cidr}]}],
                            'TagSpecifications': [{'ResourceType': 'security-group-rule', 'Tags': [{'Key': 'bdd', 'Value': 'true'}]}]
                            }

    logger.info("---------------------------------")
    logger.info("Making API call")
    logger.info("---------------------------------")
    response = requests.request(method, context.url, **kwargs, json=context.request_body)
    logger.info("---------------------------------")
    logger.info("Response: %s", response)
    logger.info("Response details: %s", response.text)
    logger.info("Response headers: %s", response.headers)
    logger.info("Response url: %s", response.url)

    context.status_code = response.status_code
    context.response_data = (json.loads(response.text))


@when(u'we invoke the generic boto3 API with an invalid request')
def step_impl(context):
    """
    Invoke the POST Boto3 Proxy API
    """
    logger.info("Invoking API")
    headers = {
        'authorization': context.token,
        'Host': context.api_host
    }
    kwargs = {
        'headers': headers
    }
    method = 'POST'

    # Empty request body in this case will fail because the action request an input in the request
    context.request_body = {}

    logger.info("---------------------------------")
    logger.info("Making API call")
    logger.info("---------------------------------")
    response = requests.request(method, context.url, **kwargs, json=context.request_body)
    logger.info("---------------------------------")
    logger.info("Response: %s", response)
    logger.info("Response details: %s", response.text)
    logger.info("Response headers: %s", response.headers)
    logger.info("Response url: %s", response.url)

    context.status_code = response.status_code
    context.response_data = (json.loads(response.text))


@then(u'API returns a status code of 200')
def step_impl(context):
    """
    Assert that the API response code is 200
    :param context:
    :return:
    """
    assert_that(context.status_code, equal_to(200))


@then(u'API returns a status code of 500')
def step_impl(context):
    """
    Assert that the API response code is 500
    :param context:
    :return:
    """
    assert_that(context.status_code, equal_to(500))


@then(u'the response contains a message of API action has been successfully completed')
def step_impl(context):
    """Assert the message returned by the API
    """

    # need to add a little delay to catch up invoking the action on the security group by the policy lambda function
    time.sleep(DEFAULT_DELAY_SECONDS)

    assert_that(
        context.response_data,
        equal_to(
            {
                'message': 'API action has been successfully completed'
            }
        )
    )

    # Check that the expected Boto3 operation was successful

    # Get the security group rule
    rules = context.ec2_client.describe_security_group_rules(Filters=[{'Name': 'group-id', 'Values': [context.security_group_id]},
                                                                      {'Name': 'tag:bdd', 'Values': ['true']}])

    logger.info(rules)

    # Should get only 1 rule back that is tagged as 'bdd'
    assert(len(rules['SecurityGroupRules']) == 1)

    # Assert the properties of the rule
    rule = rules['SecurityGroupRules'][0]
    assert (rule['GroupId'] == context.security_group_id)
    assert (rule['FromPort'] == context.from_port)
    assert (rule['ToPort'] == context.to_port)
    assert (rule['CidrIpv4'] == context.cidr)


@then(u'the response contains a message from the underlying Boto3 API')
def step_impl(context):
    """Log the message returned by the underlying Boto3 API
    """
    logger.info(context.response_data)
