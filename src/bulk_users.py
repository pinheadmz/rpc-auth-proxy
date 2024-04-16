import argparse
import json
import os
import random
import string

from werkzeug.security import generate_password_hash

# Parse command line arguments for username and optional password
parser = argparse.ArgumentParser(description="Add user and hashed password to JSON file.")
parser.add_argument("user_count", type=int, help="Number of users to generate")
parser.add_argument("-l", "--password_length", type=int, default=12, help="Length of the generated password")
args = parser.parse_args()

# Generate and save user credentials to a text file
with open("users_pass.txt", "w") as user_pass_file:
    users = {}
    for i in range(args.user_count):
        # Generate username
        username = f"user_{i+1:03d}"

        # Generate password
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(args.password_length))

        # Write user and password to the file
        user_pass_file.write(f"Username: {username}, Password: {password}\n")

        # Add user and hashed password to dictionary
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password

# Output message
print(f"{args.user_count} users and passwords have been generated and saved to users_pass.txt.")

# File to store hashed passwords
PASSWORD_FILE_PATH = "passwords.json"

# Load existing data from file
if os.path.exists(PASSWORD_FILE_PATH):
    with open(PASSWORD_FILE_PATH, 'r') as file:
        try:
            existing_users = json.load(file)
        except json.JSONDecodeError:
            existing_users = {}
else:
    existing_users = {}

# Add or update user passwords
existing_users.update(users)

# Write back to the file
with open(PASSWORD_FILE_PATH, 'w') as file:
    json.dump(existing_users, file, indent=4)

# Output message
print(f"{args.user_count} users and passwords have been added to {PASSWORD_FILE_PATH}.")
