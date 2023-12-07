import os
import sys
import sqlite3
import configparser
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    CURRENT_PATH = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_PATH = os.path.normpath(os.path.join(CURRENT_PATH, '..'))

# CONFIG FILE
config_filename = os.path.join(CURRENT_PATH, 'config.ini')
config_obj = configparser.ConfigParser()
config_obj.read(config_filename)

CLIENT_ID = config_obj['API_SETTING']['clientid']
CLIENT_SECRET = config_obj['API_SETTING']['clientsecret']

app.config['JWT_SECRET_KEY'] = CLIENT_SECRET
jwt = JWTManager(app)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify('App is not registered!'), 404

# Import and register blueprints


# Start blueprint: demo
from app.demo.demo.routes import demo_bp
app.register_blueprint(demo_bp, url_prefix=f'/featureapi/v1/demo')
# End blueprint: demo


# Start blueprint: featuresecurity
from app.featuresecurity.featuresecurity.routes import featuresecurity_bp
app.register_blueprint(featuresecurity_bp, url_prefix=f'/featureapi/v1/featuresecurity')
# End blueprint: featuresecurity

