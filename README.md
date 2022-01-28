# Execute adhoc Boto3-client operations in a multi-account AWS Organizations implementation
This project contains a centralized API that can invoke a set of approved Boto3 client operations on AWS account resources in a multi-account AWS Organizations implementation.

## Features of the API:
* This generic API allows access to only a predefined set of Boto3 actions. Those predefined actions will be stored in a parameter in AWS Systems Manager(SSM) Parameter store. 
* One SSM parameter per service is used to store a comma separated string of allowed Boto3 actions
* Example SSM param key for EC2 service= "/vpcx/aws/boto3-proxy/allowed-actions/ec2"
* The SSM param value will be in the following format:  {"authorize_security_group_ingress","authorize_security_group_egress","revoke_security_group_egress","revoke_security_group_ingress"} 
The values represent the actual Boto3 client's function name for the service. 
* If the parameter entry is missing, "invalid service" error message will be returned

## Specific use-case implemented in this project: 
A baseline set of VPC security groups can be deployed by a AWS Network Firewall policy from a central management account, and this Network Firewall policy can be applied to all workload accounts so a set of baseline security group rules is deployed in all workload accounts. 
Application teams/users may require additional security group rule(s) or exceptions to the baseline security groups rules for some applications in specific workload accounts.
This API provides automation of creating additional or exception inbound or outbound security group rules in any given account once the rule is approved.

## Architecture
![Architecture2](docs/arch.png)

## Directory structure
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

---
## Local env setup and configuration

```
# Install Python3.6, Pip, Pipenv, Nodejs >= v14

# Install python dependencies
pipenv install
pipenv shell

# Install Serverless framework
npm i -g serverless

# Install Serverless dependencies
cd boto3-proxy-api-sls
npm i

# Install serverless plugins; python 3.6 should already be installed
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-deployment-bucket

# Configure AWS named profile
aws configure --profile default 

```

## Test
```shell script
pytest ./
```

## Deployment
```shell script
# Deploy API
serverless deploy -s dev --aws-profile default
```

## Integration Test
```
behave boto3_proxy/tests/bdd/
```

## OpenAPI Spec
The OpenAPI spec for the API is located at [docs/boto3-proxy.yml](docs/boto3-proxy.yml)

## Example Usage

```bash
# Add exception inbound/outbound security group rules in a given account

curl -X POST
     -H 'Content-Type: application/json' 
     -H 'authorization: Bearer AMvcMSfZoAHnlXX0cAIhAKsJx8Pp' 
     -d { IpPermissions = [ { 'FromPort': 123, 'IpProtocol': 'string', 'IpRanges': [ { 'CidrIp': 'string', 'Description': 'string' }, ], 'Ipv6Ranges': [ { 'CidrIpv6': 'string', 'Description': 'string' }, ], 'ToPort': 123 }, ], TagSpecifications=[ { 'ResourceType': 'security-group-rule, 'Tags': [ { 'Key': 'vpcx:skip_enforcement', 'Value': 'yes' }, ] }, ], }
https://vpce-01227fc69-kykwwlo6.execute-api.us-east-1.vpce.amazonaws.com/dev/v1/accounts/itx-016/regions/us-east-1/services/ec2/actions/authorize_egress
```

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
