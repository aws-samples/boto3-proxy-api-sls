"""
this module contains behave framework function implementation
"""
# pylint:disable=no-name-in-module,import-error, C0413, C0411

import os
import sys
from random import randint

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '')))

THISDIR = os.path.dirname(__file__)  # bdd/
TESTDIR = os.path.dirname(THISDIR)  # tests/
LAMBDADIR = os.path.dirname(TESTDIR)  # boto3-proxy/
APPDIR = os.path.dirname(LAMBDADIR)  # boto3-proxy/
SERVERLESSDIR = os.path.dirname(APPDIR)  # serverless_2/
ROOTDIR = os.path.dirname(SERVERLESSDIR)  # awsapi/

sys.path.insert(0, THISDIR)
sys.path.insert(0, TESTDIR)
sys.path.insert(0, LAMBDADIR)
sys.path.insert(0, SERVERLESSDIR)
sys.path.insert(0, ROOTDIR)

from tests import config, logger, shared_config
from serverless.bdd_utils import utils


def before_all(context):
    """
    This method runs before all
    Args:
        context:
    Returns:
    """
    # environment variables for app

    logger.info("======================")
    logger.info("IN BEFORE")
    logger.info("======================")

    context.token_url = config['main']['token_url']
    context.account = config['main']['account']
    context.region = config['main']['region']
    context.application_endpoint = config['oauth2']['application_vpc_endpoint']
    context.application_scope = config['oauth2']['application_scope']
    context.application_account = config['main']['admin_account']
    context.test_account = config['main']['account']
    context.test_account_id = config['main']['account_id']
    context.stack_name = f"boto3-proxy-{config['main']['environment']}"
    context.client_id = shared_config['behave']['jenkins_client_id']
    context.client_secret = shared_config['behave']['jenkins_client_secret']
    context.creds_host = shared_config['behave']['creds_host']
    context.creds_endpoint = shared_config['behave']['creds_vpc_endpoint']
    context.creds_scope = shared_config['behave']['creds_scope']

    context.api_client = utils.ApiRequests(context.token_url, context.client_id, context.client_secret)

    context.api_host = utils.get_serverless_api_host(context.stack_name,
                                                     context.application_account,
                                                     config['main']['environment'])
    logger.info(f"API HOST: {context.api_host}")

    # Create a test security group
    context.vpc_id = config['behave']['vpc_id']
    context.ec2_client = utils.connect_service('ec2', context.account, region=context.region)

    response = context.ec2_client.create_security_group(
        GroupName='security-group-for-boto3-proxy-tests-' + str(randint(1, 999)),
        Description='Security Group for Boto3 Proxy BDD tests',
        VpcId=context.vpc_id)

    # Save the Security Group ID
    context.security_group_id = response['GroupId']


def after_all(context):
    """
    Cleanup all the resources created by the BDD for testing
    """
    # Delete the Security Group created by the Positive Scenario
    if hasattr(context, 'security_group_id'):
        try:
            # delete the security groups
            logger.info('Deleting the security group: %s', context.security_group_id)
            context.ec2_client.delete_security_group(GroupId=context.security_group_id)
        except Exception as error:
            logger.error(f'Error in deleting security group {error}')
            return
