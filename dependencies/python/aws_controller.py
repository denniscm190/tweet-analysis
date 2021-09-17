import boto3
import base64
import json
from botocore.exceptions import ClientError


class AwsSecretsManager:
    @staticmethod
    def get_secret(secret_name, region_name='eu-west-2'):
        """
        Get Secret Keys from AWS Secrets Manager
        :return:
        """

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # AWS Can't find the resource that you asked for.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

            return json.loads(secret)


class AwsComprehend:

    @staticmethod
    def get_sentiment(tweets):
        """
        :param tweets: list (string), required
        :return: dict
        """
        # Create a Comprehend client
        session = boto3.session.Session()
        comprehend = session.client(
            service_name='comprehend',
            region_name='eu-west-2'
        )

        response = comprehend.batch_detect_sentiment(
            TextList=tweets,
            LanguageCode='en'
        )

        return response
