# Centralized Boto3 proxy for adhoc operations
This project contains a centralized API that can invoke allowed boto3 client operations on AWS account resources in a multi-account AWS Organizations implementation.

## Features of the API:
* This generic API allows access to only a predefined list of boto3 actions. Those predefined actions will be stored in a parameter in Systems Manager Parameter store. 
* One SSM parameter per service with a string  of allowed boto3 actions
* Example param key for EC2 service= "/vpcx/aws/boto3-proxy/allowed-actions/ec2"
* The value will be in the following format:  {"authorize_security_group_ingress","authorize_security_group_egress","revoke_security_group_egress","revoke_security_group_ingress"} 
The values represent the actual boto3 client's function name for the service. 
* If the parameter entry is missing, "invalid service" error message will be returned

## Usecase: 
Centralized governance and compliance of accounts is enforced by ISRM security guidelines, cloud conformity governance rules, and other best practices on AWS resources. 
Application teams/end customers require additional security group rule(s) which need to be configured to enable communication for applications with other aws resources. 
This API allows automation of creating exception inbound or outbound security group rules in any given account once an exception is approved.

```
.
├── README.md                           <-- This documentation file
├── boto3_proxy                         <-- Lambda function that invokes the boto3 client action
├── utils                               <-- shared functions
├── config                              <-- configuration params
├── docs                                <-- OpenAPI doc 
├── Pipfile                             <-- Python dependencies
└── serverless.yml                      <-- Serverless application definition file
```
## Pre-requisites
```shell script
Install NodeJS
Install Serverless framework
Install Python 3.6, Pip3
```

## Test
```shell script
#Install Python requirements
pip3 install -r requirements.txt

pytest ./
```

## Deployment
```shell script
# Install serverless framework dependencies from package.json
npm i

# Deploy API
serverless deploy -s dev
```

## Integration Test
```
behave boto3_proxy/tests/bdd/
```

## OpenAPI Spec
The OpenAPI spec for the API is located at [boto3-proxy.yml](boto3-proxy.yml)

## Example Usage

```bash
# Add exception inbound/outbound security group rules in a given account

curl -X POST
     -H 'Content-Type: application/json' 
     -H 'authorization: Bearer AMvcMSfZoAHnlXX0cAIhAKsJx8Pp' 
     -d { IpPermissions = [
        {
            'FromPort': 123,
            'IpProtocol': 'string',
            'IpRanges': [
                {
                    'CidrIp': 'string',
                    'Description': 'string'
                },
            ],
            'Ipv6Ranges': [
                {
                    'CidrIpv6': 'string',
                    'Description': 'string'
                },
            ],
            'ToPort': 123
        },
    ],
    TagSpecifications=[
        {
            'ResourceType': 'security-group-rule,
            'Tags': [
                {
                    'Key': 'vpcx:skip_enforcement',
                    'Value': 'yes'
                },
            ]
        },
    ],
}
     https://vpce-01227fc69-kykwwlo6.execute-api.us-east-1.vpce.amazonaws.com/dev/v1/accounts/itx-016/regions/us-east-1/services/ec2/actions/authorize_egress
```

## License
This library is licensed under the MIT-0 License. See the LICENSE file.