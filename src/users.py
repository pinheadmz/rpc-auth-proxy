import argparse
import json
import os
import random
import string

from werkzeug.security import generate_password_hash

from config import password_file_path

# Parse command line arguments for username and optional password
parser = argparse.ArgumentParser(description="Add user and hashed password to JSON file.")
parser.add_argument("username", type=str, help="Username to add")
parser.add_argument("-p", "--password", type=str, help="Optional password")
args = parser.parse_args()

# Generate a secure password if not provided
if args.password:
    password = args.password
else:
    password_length = 12
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(password_length))

# Hash the password
hashed_password = generate_password_hash(password)

# File to store hashed passwords
PASSWORD_FILE_PATH = password_file_path()

# Load existing data from file
if os.path.exists(PASSWORD_FILE_PATH):
    with open(PASSWORD_FILE_PATH, 'r') as file:
        try:
            users = json.load(file)
        except json.JSONDecodeError:
            users = {}
else:
    users = {}

# Add or update user password
users[args.username] = hashed_password

# Write back to the file
with open(PASSWORD_FILE_PATH, 'w') as file:
    json.dump(users, file, indent=4)

# Output the generated or provided password to the terminal
print(f"Password for {args.username}: {password}")
