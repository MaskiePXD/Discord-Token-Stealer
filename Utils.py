import json
from logger import logger
from constants import TOKENS_FILE_NAME


def saveToken(newToken: str) -> bool:
    logger.info(f"Saving token: {newToken}")
    json_data = {"TOKENS": []}  # Default structure in case the file doesn't exist
    
    try:
        # Try to load the existing tokens file
        logger.info("Attempting to load the existing tokens file.")
        with open(TOKENS_FILE_NAME, "r") as file:
            json_data = json.load(file)
        
        # Append the new token to the list if it's not already present
        if newToken not in json_data["TOKENS"]:
            json_data["TOKENS"].append(newToken)
        else:
            logger.info("Token already exists in the file.")

    except FileNotFoundError:
        logger.warning(f"{TOKENS_FILE_NAME} not found. Creating a new file.")
        json_data["TOKENS"].append(newToken)

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}. Creating a new file.")
        json_data["TOKENS"].append(newToken)

    # Write the updated tokens back to the file
    try:
        with open(TOKENS_FILE_NAME, "w") as file:
            json.dump(json_data, file, indent=4)
        logger.info("Token saved successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to save the token: {e}")
        return False
