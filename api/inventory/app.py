from flask import Flask
from flask_cors import CORS

import utils
from db import db, migrate

def create_app():
    app = Flask(__name__)

    # Enabling CORS on all routes
    CORS(app, origins=['*'], methods=['^'], allow_headers=['*'])

    # Generat app configuraions
    app.secret_key = utils.get_env_value('SECRET_KEY')
    # app.config['JWT_SECRET_KEY'] = utils.get_env_value('SECRET_KEY')

    # Set up database and migrations
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.get_env_value('DATABASE_URL')
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from api.inventory import models
    
    # Initialize app routes
    from api.inventory.urls import inventory_blueprint
    app.register_blueprint(inventory_blueprint)
    
    return app

app = create_app()

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
