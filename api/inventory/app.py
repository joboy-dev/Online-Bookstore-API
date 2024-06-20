from flask import Flask

from db import db, migrate

app = Flask(__name__)

# Run application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
