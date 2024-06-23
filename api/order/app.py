from flask import Flask
import pika
import pika.exceptions

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# Set up RabbitMQ channel
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
    print('Connection successful- Order service')
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')
    

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
