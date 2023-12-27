import argparse
import json
import os
import random
import string

from werkzeug.security import generate_password_hash

from config import password_file_path

# File to store hashed passwords
PASSWORD_FILE_PATH = password_file_path()

USERNAME_PREFIX = "user_"

# Parse command line arguments for username and optional password
parser = argparse.ArgumentParser(description="Add user and hashed password to JSON file.")
parser.add_argument("-u", "--username", type=str,               help="Username to add")
parser.add_argument("-p", "--password", type=str,               help="Optional password")
parser.add_argument("-n", "--n",        type=int, default=0,    help="Number of user/pw pairs to (re)generate")
args = parser.parse_args()

if args.username is not None:
    if args.n > 1:
        raise Exception("Can not specify username for more than one new user")
    args.n = 1
if args.n > 1 and args.password is not None:
    raise Exception("Can not specify password for more than one new user")
if args.n == 0:
    raise Exception("Nothing to do")

# Load existing data from file
if os.path.exists(PASSWORD_FILE_PATH):
    with open(PASSWORD_FILE_PATH, 'r') as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}
else:
    users = {}

for i in range(args.n):
    # Compute username
    username = args.username if args.username is not None else f"{USERNAME_PREFIX}{i:03}"

    # Generate a secure password if not provided
    if args.password:
        password = args.password
    else:
        password_length = 12
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(password_length))

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Add or update user password
    users[username] = hashed_password

    # Output
    print(f"{username}, {password}")

# Write back to the file
with open(PASSWORD_FILE_PATH, 'w') as file:
    json.dump(users, file, indent=4)
