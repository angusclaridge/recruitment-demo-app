import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = 'Candidate'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        response = table.scan()  # Use scan() to get all items
        items = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error retrieving items',
                'error': str(e)
            })
        }
