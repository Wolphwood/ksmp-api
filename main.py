from modules.globals import *;

from flask import Flask;
from flask_cors import CORS

app = Flask(__name__);
CORS(app, resources={r"/ksmp-api/*": {"origins": "*"}})

from api.v1 import *;
from api.v2 import *;

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=8080);