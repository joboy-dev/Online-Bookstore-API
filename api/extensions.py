from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

socketio = SocketIO(cors_allowed_origins='*')
jwt_manager = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS(origins=['*'], methods=['^'], allow_headers=['*'])
bcrypt = Bcrypt()
