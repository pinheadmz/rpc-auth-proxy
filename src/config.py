import os
from pathlib import Path

FILENAME = ".rpc-auth-proxy-passwords.json"

def password_file_path():
    return Path(os.path.expanduser("~")) / FILENAME
