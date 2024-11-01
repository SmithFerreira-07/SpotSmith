import configparser
from cryptography.fernet import Fernet
import os


config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
key_path = os.path.join(config_dir, "encryption_key.key")
config_path = os.path.join(config_dir, "config.ini")

def load_key():
    with open(key_path, "rb") as key_file:
        return key_file.read()

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

def load_decrypted_credentials():
    key = load_key()
    config = configparser.ConfigParser()
    config.read(config_path)

    encrypted_client_id = config["SPOTIFY"]["client_id"]
    encrypted_client_secret = config["SPOTIFY"]["client_secret"]

    client_id = decrypt_data(encrypted_client_id, key)
    client_secret = decrypt_data(encrypted_client_secret, key)

    return client_id, client_secret
