from flask import Flask

from db import db, migrate

from api import utils

app = Flask(__name__)

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
