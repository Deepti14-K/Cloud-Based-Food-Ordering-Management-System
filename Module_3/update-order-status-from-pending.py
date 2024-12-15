import json
import boto3 
import random
import base64
from boto3.dynamodb.conditions import Key, Attr

dynamodb_client = boto3.resource('dynamodb')
dynamodb_table_name = 'orders-table'


def lambda_handler(event, context):

    """ Based on the order_id and status received, update the order status in the DynamoDB table"""
    
    try:
        status = event.get('status', '')
        order_id = event.get('order_id', '')
        table = dynamodb_client.Table(dynamodb_table_name)
        if status != '' and order_id != '':
            order_status = "SUCCESS"
            if status == "error":
                order_status = "FAILED"
                
            response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('order_id').eq(order_id))
            if len(response['Items']) == 1:
                response = table.update_item(
                    Key={'order_id': order_id},
                    UpdateExpression="set order_status=:s",
                    ExpressionAttributeValues={
                        ':s': order_status
                    },
                    ReturnValues="UPDATED_NEW")
                
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {
                        'status_code': 200,
                        'body': "Order status for order_id {} is updated to {}".format(order_id, order_status)
                    }
                    
        return {
            'status_code': 400,
            'body': "Either order_id is incorrect or status was not determined"
        }
        
    except Exception as e:
         return {
            'status_code': 500,
            'body': "Unable to update status to due an internal server error"
        }
