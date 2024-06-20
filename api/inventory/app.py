from flask import Flask
import pika, json
import pika.exceptions

app = Flask(__name__)

# RabbitMQ connection
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be received')
    

# Set up callback function to perform an action with the rev=ceived data
def callback(ch, method, properties, body):
    '''Callback method'''
    
    from db import db
    from api.inventory import models
    
    order_message = json.loads(body)
    
    book_id = order_message['book_id']
    quantity = order_message['quantity']
    
    inventory_item = db.session.query(models.Inventory).filter(book_id == book_id).first()
    
    if not inventory_item:
        print('Inventory item not found')
    
    inventory_item.stock_quantity -= quantity
    db.session.commit()
    
    print('Inventory updated successfully')
    
# Start data consumption process
channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
