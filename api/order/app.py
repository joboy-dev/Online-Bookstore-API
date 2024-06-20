from flask import Flask
from flask_socketio import SocketIO
import pika
import pika.exceptions

app = Flask(__name__)
socketio = SocketIO(app)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')
    
channel = connection.channel()
channel.queue_declare(queue='order_queue', durable=True)

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
