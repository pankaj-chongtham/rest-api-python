import os
import sys
import sqlite3
import argparse
import fileinput
import traceback
import configparser
from datetime import datetime
from app import featurelog
from server import BASE_PREFIX

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    CURRENT_PATH = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

app_log = featurelog.setup_logger()

# CONFIG FILE
config_filename = os.path.join(CURRENT_PATH, 'config.ini')
config_obj = configparser.ConfigParser()
config_obj.read(config_filename)

try:
    conn = sqlite3.connect('feature.db')
    cursor = conn.cursor()
    # Create a table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS client_info (
                    clientid TEXT PRIMARY KEY,
                    clientsecret TEXT NOT NULL,
                    createddate DATETIME
                )''')
    conn.commit()
except Exception as e:
    app_log.error(e)
    app_log.error(traceback.format_exc())


def check_clientid_exists(cursor, clientid):
    cursor.execute('SELECT clientid FROM client_info WHERE clientid = ?', (clientid,))
    result = cursor.fetchone()  # Fetch one row, if any
    return result is not None


def deregister_app(app_name):
    try:
        init_file_path = os.path.join(CURRENT_PATH, 'app', '__init__.py')

        # Define a start and end marker for the lines to remove
        start_marker = f"# Start blueprint: {app_name}\n"
        end_marker = f"# End blueprint: {app_name}\n"

        with fileinput.FileInput(init_file_path, inplace=True) as file:
            inside_blueprint = False

            for line in file:
                if line == start_marker:
                    inside_blueprint = True
                elif line == end_marker:
                    inside_blueprint = False

                elif not inside_blueprint:
                    print(line, end='')
        if not inside_blueprint:
            print(f'{app_name} is not registered!')
        else:
            print(f"Deregistered app: {app_name} Successfully")
    except Exception as e:
        app_log.error(e)
        app_log.error(traceback.format_exc())

def register_app(app_name):
    try:
        init_file_path = os.path.join(CURRENT_PATH, 'app', '__init__.py')
        app_blueprint = f"\n\n# Start blueprint: {app_name}" \
                        f"\nfrom app.{app_name}.{app_name}.routes import {app_name}_bp" \
                        f"\napp.register_blueprint({app_name}_bp, url_prefix=f'{BASE_PREFIX}/{app_name}')" \
                        f"\n# End blueprint: {app_name}\n"
        with fileinput.FileInput(init_file_path, inplace=True) as file:
            for line in file:
                print(line, end='')
                if line.strip() == "# Import and register blueprints":
                    print(app_blueprint, end='')
        print(f"Registered app: {app_name} Successfully")
    except Exception as e:
        app_log.error(e)
        app_log.error(traceback.format_exc())


def deregister_client():
    try:
        sqlite3_conn = sqlite3.connect('feature.db')
        cursor = sqlite3_conn.cursor()
        clientid = input("Enter the client ID to deregister: ")

        # Check if the client ID exists
        if check_clientid_exists(cursor, clientid):
            # Prompt the user for confirmation
            deregister_verification = input(
                f"Do you want to deregister the client '{clientid}'? (yes/no): ").lower()

            if deregister_verification in ['yes', 'y']:
                # Perform the deletion
                cursor.execute('DELETE FROM client_info WHERE clientid = ?', (clientid,))
                sqlite3_conn.commit()
                print(f"Client ID '{clientid}' deregistered successfully.")
            else:
                print("Deregistration canceled.")
        else:
            print(f"Client ID '{clientid}' does not exist in the database.")
    except Exception as e:
        app_log.error(e)
        app_log.error(traceback.format_exc())


def is_app_name_available(app_name):
    app_root_dir = os.path.join(CURRENT_PATH, 'app', app_name)
    return not os.path.exists(app_root_dir)

def create_app(app_name):
    # Define the directory structure
    if not is_app_name_available(app_name):
        print(f"Error: '{app_name}' already exists.")
        return

    app_root_dir = os.path.join(CURRENT_PATH, 'app', app_name)
    inner_dir = os.path.join(app_root_dir, app_name)

    # Create the directories
    os.makedirs(inner_dir, exist_ok=True)

    # Create __init__.py
    init_file_path = os.path.join(inner_dir, '__init__.py')
    with open(init_file_path, 'w') as init_file:
        pass  # Empty __init__.py file

    # Create routes.py
    routes_file_path = os.path.join(inner_dir, 'routes.py')
    with open(routes_file_path, 'w') as routes_file:
        routes_file.write(
            f"from flask import Blueprint, jsonify\n"
            f"from flask_jwt_extended import jwt_required\n\n"
            f"{app_name}_bp = Blueprint('{app_name}', __name__)\n\n"
            f"@{app_name}_bp.route('/ping')\n"
            f"@jwt_required()\n"
            f"def ping():\n"
            f"    return jsonify({{'message': f'You are reaching {app_name} Application.'}})\n"
        )

    print(f"App '{app_name}' created successfully at {app_root_dir}")


def register_client():
    try:
        clientid = config_obj['API_SETTING']['clientid']
        clientsecret = config_obj['API_SETTING']['clientsecret']
        # Print the values for verification
        print(f"Client ID: {clientid}")
        print(f"Client Secret: {clientsecret}")

        # Ask the user for verification
        verification = input("Are these values correct? (yes/no): ").lower()

        if verification in ['yes', 'y']:
            if check_clientid_exists(cursor, clientid):
                print(f"Client ID '{clientid}' exists in the database.")
                # Prompt the user for update confirmation
                update_verification = input("Do you want to update the client? (yes/no): ").lower()
                if update_verification in ['yes', 'y']:
                    cursor.execute('UPDATE client_info SET clientsecret = ?, createddate = ? WHERE clientid = ?',
                                   (clientsecret, datetime.now(), clientid))
                    print('Client ID Updated!')
            else:
                cursor.execute('INSERT INTO client_info(clientid, clientsecret, createddate) VALUES '
                               '(?, ?, ?)', (clientid, clientsecret, datetime.now())
                               )
                print('Registration Successfully!')
            conn.commit()
        else:
            print("Registration canceled.")
    except Exception as e:
        app_log.error(e)
        app_log.error(traceback.format_exc())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to register app and client.")
    # Register App command
    parser.add_argument('--register-app', action='store_true', help="Register an app")
    parser.add_argument('--deregister-app', action='store_true', help="De-Register an app")
    parser.add_argument('--create-app', action='store_true', help="Create an app")
    # Add the --name argument
    parser.add_argument('--name', help="Specify the app name")

    # Register Client command
    parser.add_argument('--register-client', action='store_true', help="Register a client")
    parser.add_argument('--deregister-client', action='store_true', help="De-Register a client")


    # Parse the command-line arguments
    args = parser.parse_args()
    app_log.info(f'args: {args}')

    # Check which flag is present and execute the corresponding code block
    if args.register_app:
        if args.name:
            app_log.info('Registering app...')
            app_name = args.name
            register_app(app_name)
        else:
            print("No app name provided.")
    elif args.deregister_app:
        if args.name:
            app_log.info('De-Registering app...')
            app_name = args.name
            deregister_app(app_name)
        else:
            print("No app name provided.")
    elif args.register_client:
        app_log.info('Registering client...')
        register_client()
    elif args.deregister_client:
        app_log.info(('De-registering client...'))
        deregister_client()
    elif args.create_app:
        if args.name:
            create_app(args.name)
        else:
            print("No app name provided")
    else:
        print("No valid command provided.")
