from flask import Flask, render_template
from flask_socketio import SocketIO
import pika
import pika.exceptions

def create_app():
    app = Flask(__name__)
    
    from order.urls import order_blueprint
    app.register_blueprint(order_blueprint)
    
    return app


app = create_app()
socketio = SocketIO(app, cors_allowed_origins='*')

# Test socketio connection
@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    socketio.emit('response', {'data': 'Backend: Message received!'})
    

@app.route('/')
def index():
    return render_template('order-notifications.html')


# Set up RabbitMQ channel
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue', durable=True)
except pika.exceptions.AMQPConnectionError:
    print('Failed to connect to RabbitMQ service. Message won\'t be sent')
    

# Run application
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001, debug=True)
