import json
import random 

def lambda_handler(event, context):
    
    """ The function simulates the result of the restaurant accepting the order;
    proabability of success is 80%, failure is 20% """
    
    status = random.choices(["ok", "error"], weights=(80, 20), k=1)[0]
    
    return {
        'status_code': 200,
        'order_id' : event.get('order_id', ''),
        'function' : 'restaurant',
        'status' : status
    }
