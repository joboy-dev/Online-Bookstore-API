from flask import Flask, render_template
import pika
import pika.exceptions

from api.extensions  import socketio

def create_app():
    app = Flask(__name__)
    return app


app = create_app()


# Test socketio connection
@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    socketio.emit('response', {'data': 'Backend: Message received!'})


# Set up RabbitMQ channel
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')
    

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
