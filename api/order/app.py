from flask import Flask
import pika
import pika.exceptions

from api import utils

app = Flask(__name__)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')
    
channel = connection.channel()
channel.queue_declare(queue='order_queue', durable=True)

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
