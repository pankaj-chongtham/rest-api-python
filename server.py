import os
import sys
import configparser
from app import app
from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

__VERSION__ = 'v1.0'
BASE_PREFIX = '/featureapi/v1'

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    CURRENT_PATH = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# CONFIG FILE
config_filename = os.path.join(CURRENT_PATH, 'config.ini')
config_obj = configparser.ConfigParser()
config_obj.read(config_filename)

jwtenabled = config_obj.getboolean('API_SETTING', 'jwtenabled')

@app.route(f'{BASE_PREFIX}/version')
def ping():
    return jsonify({'productVersion': __VERSION__})


if __name__ == '__main__':
    app.run(debug=True)
