import sqlite3
from app import app
from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

__VERSION__ = 'v1.0'

BASE_PREFIX = '/featureapi/v1'

@app.route(f'{BASE_PREFIX}/version')
def ping():
    return jsonify({'productVersion': __VERSION__})


if __name__ == '__main__':
    app.run(debug=True)
