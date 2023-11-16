import argparse
import datetime
import json
import os
import requests
import subprocess

from flask import Flask, request, jsonify, make_response
from werkzeug.security import check_password_hash

from config import password_file_path

LOCAL_RPC_PASSWORD = "3c66d9b5be9ba72ff32f2e412db6da9dcf7cae5a223f04ba675445b1a8c4cf07"

DISALLOWED_METHODS = [
    "invalidateblock",
    "pruneblockchain",
    "preciousblock",
    "setban",
    "addnode",
    "stop"
]

RPC_PORTS = {
#               [listen, bitcoin]
    "main":     [8332, 8330],
    "testnet":  [18332, 18330],
    "signet":   [38332, 38330],
    "regtest":  [18443, 18440]
}

PASSWORD_FILE_PATH = password_file_path()

app = Flask(__name__)

def log(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Function to validate credentials
def validate_credentials(username, password):
    # Load hashed passwords from file
    with open(PASSWORD_FILE_PATH, "r") as file:
        hashed_passwords = json.load(file)

    # Check if username exists and password matches
    return (username in hashed_passwords and
            check_password_hash(hashed_passwords[username], password))

@app.route('/', methods=['POST'])
def root():
    return handle_request('')

@app.route('/<path:endpoint>', methods=['POST'])
def endpoint(endpoint):
    return handle_request(endpoint)

def handle_request(endpoint):
    auth = request.authorization
    if not auth or not validate_credentials(auth.username, auth.password):
        log(f"Failed auth by: {auth.username}")
        return make_response('Could not verify login!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    # Parse the JSON RPC request
    rpc_request = request.get_json()

    if isinstance(rpc_request, list):
        for call in rpc_request:
            if call["method"] in DISALLOWED_METHODS:
                log(f"Unauthorized method by {auth.username}: {call['method']}")
                return jsonify({"error": "Method not allowed"}), 403
    else:
        if rpc_request["method"] in DISALLOWED_METHODS:
            log(f"Unauthorized method by {auth.username}: {rpc_request['method']}")
            return jsonify({"error": "Method not allowed"}), 403

    # Construct the URL for the local RPC server with the same endpoint
    local_rpc_url = f"http://:{LOCAL_RPC_PASSWORD}@localhost:{os.environ['LOCAL_PORT']}/{endpoint}"

    # Forward the request to the local JSON RPC server
    response = requests.post(local_rpc_url, json=rpc_request)
    log(f"Request by {auth.username} ({response.status_code}): {rpc_request}")

    return jsonify(response.json())

if __name__ == '__main__':
    # Parse command line arguments for the network (port number)
    parser = argparse.ArgumentParser(description="Run a JSON-RPC proxy server.")
    parser.add_argument("network", type=str, help="Which Bitcoin network to proxy to")
    args = parser.parse_args()
    if args.network not in RPC_PORTS:
        raise Exception("Unknown network")

    subprocess.run(
        [
            "gunicorn",
            "-w", "4",
            "--timeout", "600",
            f"-b :{RPC_PORTS[args.network][0]}",
            "server:app"
        ],
        env={**os.environ, "LOCAL_PORT": f"{RPC_PORTS[args.network][1]}"},
        cwd=os.path.dirname(os.path.realpath(__file__)))
