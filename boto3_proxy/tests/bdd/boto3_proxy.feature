@integration_test
@ABGN-8491-generic-boto3-api

Feature: Generic boto3 API used by exception APIs

  Scenario: Positive scenario 1 - Successful completion of boto3 actions
    Given the API POST /v1/accounts/<bdd_account>/regions/us-east-1/services/ec2/actions/authorize_security_group_ingress exists
    And valid oauth2 token for API authorization is generated
    And the VPCx account bdd_account is valid
    When we invoke the generic boto3 API with a valid request
    Then API returns a status code of 200
    And the response contains a message of API action has been successfully completed

  Scenario: Negative scenario 1 - Invalid request
    Given the API POST /v1/accounts/<bdd_account>/regions/us-east-1/services/ec2/actions/authorize_security_group_ingress exists
    And valid oauth2 token for API authorization is generated
    And the VPCx account bdd_account is valid
    When we invoke the generic boto3 API with an invalid request
    Then API returns a status code of 500
    And the response contains a message from the underlying Boto3 API