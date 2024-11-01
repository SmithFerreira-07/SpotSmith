import configparser
from cryptography.fernet import Fernet
import os
from rich import print


config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config'))
key_path = os.path.join(config_dir, "encryption_key.key")
config_path = os.path.join(config_dir, "config.ini")


def generate_key():
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        os.makedirs(config_dir, exist_ok=True)
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        print("Encryption key already exists.")


def load_key():
    with open(key_path, "rb") as key_file:
        return key_file.read()


def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def save_encrypted_credentials(client_id, client_secret):
    key = load_key()
    encrypted_client_id = encrypt_data(client_id, key)
    encrypted_client_secret = encrypt_data(client_secret, key)

    config = configparser.ConfigParser()
    config["SPOTIFY"] = {
        "client_id": encrypted_client_id,
        "client_secret": encrypted_client_secret
    }
    
    with open(config_path, "w") as config_file:
        config.write(config_file)

if __name__ == "__main__":
    generate_key()
    print('''[bold green]

        Welcome to SpotSmith Setup!        
        ⠀⠀⠀⠀⠀⠙⢷⣤⣤⣴⣶⣶⣦⣤⣤⡾⠋⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣼⣿⣿⣉⣹⣿⣿⣿⣿⣏⣉⣿⣿⣧⠀⠀⠀⠀
        ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
        ⣠⣄⠀⢠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡄⠀⣠⣄
        ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
        ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
        ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
        ⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿
        ⠻⠟⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⠻⠟
        ⠀⠀⠀⠀⠉⠉⣿⣿⣿⡏⠉⠉⢹⣿⣿⣿⠉⠉⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀


[/bold green]''')
    client_id = input("Enter Spotify Client ID: ")
    client_secret = input("Enter Spotify Client Secret: ")
    save_encrypted_credentials(client_id, client_secret)
    print("Credentials saved securely.")
