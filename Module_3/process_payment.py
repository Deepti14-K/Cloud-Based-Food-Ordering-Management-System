import json
import random 

def lambda_handler(event, context):
    
    """ The function simulates the result of a transaction; proabability of success is 95%, failure is 5% """
    
    status = random.choices(["ok", "error"], weights=(95, 5), k=1)[0]
    
    return {
        'status_code': 200,
        'order_id' : event.get('order_id', ''),
        'function' : 'payment',
        'status' : status
    }
