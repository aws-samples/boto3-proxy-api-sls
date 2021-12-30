from utils.api_gateway_response import DoubleQuoteDict
from utils.exceptions import InvalidRegionException


def is_region_valid(ec2_client, region):
    """This function checks whether the region is valid for all the services used in this lambda function.

    Args:
        ec2_client: The EC2 client authenticated for the account
        region: The region name that needs to be validated

    Returns:
      None

    Raises:
      InvalidRegionException: The exception indicating that the region name is inavlid.
    """
    response = ec2_client.describe_regions()
    regions = [region['RegionName'] for region in response['Regions']]
    if region not in regions:
        raise InvalidRegionException("Invalid region")


def lambda_returns(status_code, headers, body):
    """Create a dictionary per ApiGateway's requirements

    Args:
        status_code(int): response.status_code
        headers(dict): response.headers
        body(str): response.text

    Returns:
        ret_object : specified by aws ApiGateway
    """
    headers = DoubleQuoteDict(headers)
    ret_object = {
        'statusCode': status_code,
        'headers': headers,
        'body': body
    }
    return ret_object
