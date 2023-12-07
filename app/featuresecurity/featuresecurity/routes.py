import os
import sys
import sqlite3
import configparser
from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

featuresecurity_bp = Blueprint('securitytoken', __name__)

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    CURRENT_PATH = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_PATH = os.path.normpath(os.path.join(CURRENT_PATH, '..', '..', '..'))


def check_clientid_exists(clientid):
    sqlite3_conn = sqlite3.connect(os.path.join(CURRENT_PATH, 'feature.db'))
    cursor = sqlite3_conn.cursor()
    cursor.execute('SELECT clientid FROM client_info WHERE clientid = ?', (clientid,))
    result = cursor.fetchone()  # Fetch one row, if any
    cursor.close()
    sqlite3_conn.close()
    return result is not None  # Return True if clientid exists, False otherwise


def check_clientsecret(clientid):
    sqlite3_conn = sqlite3.connect(os.path.join(CURRENT_PATH, 'feature.db'))
    cursor = sqlite3_conn.cursor()
    cursor.execute('SELECT clientsecret FROM client_info WHERE clientid = ?', (clientid,))
    result = cursor.fetchone()[0]
    cursor.close()
    sqlite3_conn.close()
    return result


@featuresecurity_bp.route('/token')
def token():
    client_id = request.headers.get('clientid')
    client_secret = request.headers.get('clientsecret')
    if not client_id or not client_secret:
        return jsonify({"Message": "Client ID and Client Secret are required."})

    if check_clientid_exists(client_id):
        sqlite3_secret = check_clientsecret(client_id)
        if client_secret == sqlite3_secret:
            expires = timedelta(seconds=180)
            access_token = create_access_token(identity=client_id, expires_delta=expires)
            return jsonify(access_token=access_token, expires_in=f'{expires.total_seconds()} seconds')
        else:
            return jsonify({"Message": "Invalid Secret."})
    else:
        return jsonify({"Message": "Invalid Client."})


@featuresecurity_bp.route('/ping')
@jwt_required()
def ping():
    return jsonify({"message": "You are reaching 'securitytoken' Application."})