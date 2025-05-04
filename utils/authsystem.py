import uuid
import json
from utils.logger import setup_logger

FILE_PATH = "data/keys/keys.json"
logger = setup_logger()

def load_keys_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_keys_to_file(keys, file_path):
    with open(file_path, "w") as file:
        json.dump(keys, file, indent=4)

def generate_key(keys, month, amount, quantity, file_path):
    new_keys = [{"key": str(uuid.uuid4()), "month": month, "amount": amount} for _ in range(quantity)]
    keys.extend(new_keys)
    save_keys_to_file(keys, file_path)
    logger.info(f"Generated {quantity} keys for {amount}x {month} month boosts")

def delete_key(keys, key):
    updated_keys = [key_data for key_data in keys if key_data["key"] != key]
    save_keys_to_file(updated_keys, FILE_PATH)
    logger.info(f"Deleted key: {key}")

def clear_file(file_path):
    save_keys_to_file([], file_path)
    logger.info("Cleared keys file")