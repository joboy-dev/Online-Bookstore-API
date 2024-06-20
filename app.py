from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.utils import get_env_value
from db import db, migrate

def create_app():
    app = Flask(__name__)

    # Enabling CORS on all routes
    CORS(app, origins=['*'], methods=['^'], allow_headers=['*'])

    # Generat app configuraions
    app.secret_key = get_env_value('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = get_env_value('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # Set up database and migrations
    app.config['SQLALCHEMY_DATABASE_URI'] = get_env_value('DATABASE_URL')
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from api.user import models
        from api.book import models
        from api.inventory import models
        from api.order import models
        
    # Initialize jwt mamager
    jwt_manager = JWTManager(app)
    
    # Initialize app routes
    from api.user.urls import user_blueprint
    from api.book.urls import book_blueprint
    from api.inventory.urls import inventory_blueprint
    from api.order.urls import order_blueprint
    
    app.register_blueprint(user_blueprint)
    app.register_blueprint(book_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(order_blueprint)
    
    return app

app = create_app()


# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
