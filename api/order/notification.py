from uuid import UUID

from api.order import app

def send_order_notification(order_id: UUID, user_id: UUID, status, datetime_sent):
    '''Function to send order notification to a user'''
    
    data =  {
        'order_id': order_id,
        'user_id': user_id,
        'status': status,
        'datetime_sent': datetime_sent,
    }
    
    # Send data to client side
    app.socketio.emit('order status change', data)
    
    print('Order notification sent')
    print(data)
    