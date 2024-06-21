from uuid import UUID
from flask import Flask
from flask_socketio import SocketIO
import pika
import pika.exceptions

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def send_order_notification(order_id: UUID, user_id: UUID, status, datetime_sent):
    '''Function to send order notification to a user'''
    
    data =  {
        'order_id': order_id,
        'user_id': user_id,
        'status': status,
        'datetime_sent': datetime_sent,
    }
    socketio.emit('order_status_change', data)
    
    print('Order notification sent')
    print(data)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')

# Run application
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
