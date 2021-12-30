"""Unit tests for helper utils"""
import os
from unittest import TestCase
import unittest
from utils.exceptions import InvalidRegionException
from utils.api_gateway_response import DoubleQuoteDict
# pylint: disable = no-name-in-module,import-error,no-self-use,broad-except, C0413, C0411, C0330

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class MockEC2Client:
    def __init__(self):
        self.describe_regions_dict = {
            "Regions": [
                {
                    "Endpoint": "ec2.eu-north-1.amazonaws.com",
                    "RegionName": "eu-north-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-south-1.amazonaws.com",
                    "RegionName": "ap-south-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.eu-west-3.amazonaws.com",
                    "RegionName": "eu-west-3",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.eu-west-2.amazonaws.com",
                    "RegionName": "eu-west-2",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.eu-west-1.amazonaws.com",
                    "RegionName": "eu-west-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-northeast-3.amazonaws.com",
                    "RegionName": "ap-northeast-3",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-northeast-2.amazonaws.com",
                    "RegionName": "ap-northeast-2",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-northeast-1.amazonaws.com",
                    "RegionName": "ap-northeast-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.sa-east-1.amazonaws.com",
                    "RegionName": "sa-east-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ca-central-1.amazonaws.com",
                    "RegionName": "ca-central-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-southeast-1.amazonaws.com",
                    "RegionName": "ap-southeast-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.ap-southeast-2.amazonaws.com",
                    "RegionName": "ap-southeast-2",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.eu-central-1.amazonaws.com",
                    "RegionName": "eu-central-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.us-east-1.amazonaws.com",
                    "RegionName": "us-east-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.us-east-2.amazonaws.com",
                    "RegionName": "us-east-2",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.us-west-1.amazonaws.com",
                    "RegionName": "us-west-1",
                    "OptInStatus": "opt-in-not-required"
                },
                {
                    "Endpoint": "ec2.us-west-2.amazonaws.com",
                    "RegionName": "us-west-2",
                    "OptInStatus": "opt-in-not-required"
                }
            ]
        }

    def describe_regions(self):
        return self.describe_regions_dict


class TestHelpers(TestCase):

    def test_is_region_valid(self):
        """Test the method to get the validity of the given region"""
        from utils.helpers import is_region_valid
        ec2_client = MockEC2Client()
        is_region_valid(ec2_client, "us-east-1")
        self.assertRaises(InvalidRegionException, is_region_valid, ec2_client, "test-org")

    def test_lambda_returns(self):
        """Test the lambda returns method"""
        from utils.helpers import lambda_returns
        status_code = 200
        body = "Test body"
        headers = {
            'Header': 'TestHeader'
        }
        lambda_returns_object = {
            'statusCode': status_code,
            'headers': DoubleQuoteDict(headers),
            'body': body
        }
        self.assertEqual(lambda_returns_object, lambda_returns(status_code, headers, body))


if __name__ == '__main__':
    unittest.main()
