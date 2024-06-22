from flask import Flask, render_template

from utilities.files import get_env_value
from api import extensions

def create_app():
    app = Flask(__name__)

    # Generat app configuraions
    app.secret_key = get_env_value('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = get_env_value('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # Set up database and migrations
    app.config['SQLALCHEMY_DATABASE_URI'] = get_env_value('DATABASE_URL')
    
    # Initialize all needed extensions
    extensions.cors.init_app(app)
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.socketio.init_app(app)
    extensions.jwt_manager.init_app(app)

    # Initialize app routes
    from api.user.urls import user_blueprint
    from api.book.urls import book_blueprint
    from api.inventory.urls import inventory_blueprint
    from api.order.urls import order_blueprint
    
    app.register_blueprint(user_blueprint)
    app.register_blueprint(book_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(order_blueprint)
    
    with app.app_context():
        from api.user import models
        from api.book import models
        from api.inventory import models
        from api.order import models
        
    return app

app = create_app()

@app.route('/')
def index():
    return render_template('order-notifications.html')


# Run application
if __name__ == '__main__':
    extensions.socketio.run(app, host='0.0.0.0', port=8000, debug=True)
