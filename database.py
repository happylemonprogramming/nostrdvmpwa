import boto3
from botocore.exceptions import NoCredentialsError
import os

# Environment variables
awssecret = os.environ["AWS_SECRET_ACCESS_KEY"]
awsaccess = os.environ["AWS_ACCESS_KEY_ID"]

def save_to_dynamodb(user, log_status):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1', aws_access_key_id=awsaccess,
                                  aws_secret_access_key=awssecret)

        # specify your table name
        table = dynamodb.Table('lightning_login')

        # insert data into the table
        response = table.put_item(
           Item={
                'user': user, # partition key is always needed
                'log_status': log_status
            }   
        )

        print("PutItem succeeded")

    except NoCredentialsError:
        print("No AWS Credentials were found.")

def get_from_dynamodb(user):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('lightning_login')
    # print(table)

    try:
        response = table.get_item(
            Key={
                'user': user
            }
        )

    except:
        print('error')
        
    else:
        return response['Item']

def update_dynamodb(user, key, value):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1', aws_access_key_id=awsaccess,
                                  aws_secret_access_key=awssecret)

        # specify your table name
        table = dynamodb.Table('lightning_login')

        # update data in the table
        response = table.update_item(
           Key={
                'user': user,
            },
            UpdateExpression='SET #k = :v',
            ExpressionAttributeNames={
                '#k' : key
            },
            ExpressionAttributeValues={
                ':v' : value
            }
        )

        print("UpdateItem succeeded")

    except NoCredentialsError:
        print("No AWS Credentials were found.")

if __name__ == '__main__':
    user = '1234567890000'
    log_status = True

    # update_dynamodb(user, key, value)
    # save_to_dynamodb(user, log_status)
    item = get_from_dynamodb(user)
    print(item)