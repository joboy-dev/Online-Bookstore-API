from uuid import UUID
from flask import Flask
import pika, json
import pika.exceptions

from api.extensions import db
from utilities import files

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = files.get_env_value('DATABASE_URL')

db.init_app(app)


# RabbitMQ connection
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
    print('Connection successful- Inventory service')
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be received')
    

# Set up callback function to perform an action with the rev=ceived data
def callback(ch, method, properties, body):
    '''Callback method'''
    
    order_message = json.loads(body)
    print(f'(Inventory) Message received- {order_message}')
    
    with app.app_context():
        from api.inventory import models
    
        print('set db and models')
        
        book_id = order_message['book_id']
        quantity = order_message['quantity']
        
        # Convert the boo_id bacvk into a UUID value to avoid issues in the database
        inventory_item = db.session.query(models.Inventory).filter(models.Inventory.book_id == UUID(book_id)).first()
        
        if not inventory_item:
            print('Inventory item not found')
        
        inventory_item.stock_quantity -= quantity
        db.session.commit()
    
        print('Inventory updated successfully')
    
# Start data consumption process
channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)

if __name__ == "__main__":
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
