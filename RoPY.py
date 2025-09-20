import logging
from datetime import datetime
from typing import Dict, Any
import requests
import time
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Developer mode flag ---
# For developers only: Set this to True to enable developer mode
DEVELOPER_MODE = False  # Set to True for extra technical details

# Constants
API_URL = "https://users.roblox.com/v1/users/"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
MAX_ID_LENGTH = 20  # Reasonable maximum length for a Roblox user ID

def fetch_user_information(user_id: str) -> None:
    """
    Fetch data from the Roblox API and print user information.
    
    Parameters:
    user_id (str): The ID of the Roblox user.
    """
    url = f"{API_URL}{user_id}"
    
    for attempt in range(MAX_RETRIES):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            latency = end_time - start_time

            response.raise_for_status()

            data = response.json()
            user_info: Dict[str, Any] = {
                "username": data.get("name", "Unknown"),
                "display_name": data.get("displayName", "Unknown"),
                "created_date": parse_date(data.get("created", "Unknown")),
                "avatar_url": data.get("avatarUrl", "Unknown"),
                "followers_count": data.get("followersCount", "Not available"),
                "friends_count": data.get("friendsCount", "Not available"),
                "latency": f"{latency:.2f} seconds"
            }

            logger.info(f"Successfully fetched data for user ID {user_id}")
            if DEVELOPER_MODE:
                logger.debug(f"Raw data: {data}")

            display_user_info(**user_info)
            break

        except requests.exceptions.HTTPError as http_err:
            if hasattr(http_err, 'response') and http_err.response is not None:
                status_code = http_err.response.status_code
                if status_code == 429:  # Too Many Requests
                    if attempt < MAX_RETRIES - 1:
                        logger.warning(f"Rate limit hit. Waiting {RETRY_DELAY} seconds before retry...")
                        time.sleep(RETRY_DELAY)
                        continue
                logger.error(f"HTTP error occurred: {http_err}")
                print(f"Error: {status_code} - Unable to fetch user information.")
            else:
                logger.error(f"HTTP error occurred: {http_err}")
                print("Error: Unable to fetch user information.")
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying... Attempt {attempt + 1} of {MAX_RETRIES}")
                time.sleep(RETRY_DELAY)
                continue
            print("A network error occurred. Please check your internet connection.")
            break
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
            print("An unexpected error occurred. Please try again later.")
            break

def parse_date(date_str: str) -> str:
    """
    Parse and format the date string.
    
    Parameters:
    date_str (str): The date string to parse.
    
    Returns:
    str: The formatted date string.
    """
    if not date_str or date_str == "Unknown":
        return "Unknown"

    date_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date string: {date_str}")
    return "Invalid date format"

def display_user_info(username: str, display_name: str, created_date: str, avatar_url: str, followers_count: str, friends_count: str, latency: str) -> None:
    """
    Displays information about a user.
    
    Parameters:
    username (str): The username of the user.
    display_name (str): The display name of the user.
    created_date (str): The cleaned creation date of the user.
    avatar_url (str): The avatar URL of the user.
    followers_count (str): The follower count of the user.
    friends_count (str): The friend count of the user.
    latency (str): The latency of the request.
    """
    print("\nUser Information:")
    print(f"Username: {username}")
    print(f"Display Name: {display_name}")
    print(f"Created: {created_date}")
    print(f"Avatar URL: {avatar_url}")
    print(f"Followers: {followers_count}")
    print(f"Friends: {friends_count}")
    print(f"Latency: {latency}")

def validate_user_id(user_id: str) -> bool:
    """
    Validate the user ID input.
    
    Parameters:
    user_id (str): The user ID to validate.
    
    Returns:
    bool: True if valid, False otherwise.
    """
    if not user_id.strip():
        error_msg = "Error: ID cannot be empty."
        print(error_msg)
        logger.warning("User provided empty ID")
        return False
    
    if not user_id.isdigit():
        error_msg = "Error: ID must contain only numbers."
        print(error_msg)
        logger.warning(f"User provided invalid ID format: {user_id}")
        return False
        
    if len(user_id) > MAX_ID_LENGTH:
        error_msg = f"Error: ID is too long (maximum {MAX_ID_LENGTH} digits)."
        print(error_msg)
        logger.warning(f"User provided ID too long: {len(user_id)} digits")
        return False
        
    if int(user_id) <= 0:
        error_msg = "Error: ID must be a positive number."
        print(error_msg)
        logger.warning(f"User provided non-positive ID: {user_id}")
        return False
        
    return True

def main() -> None:
    """
    Main function to run the script.
    Prompts the user to enter the ID of a Roblox user and displays their information.
    """
    print("Welcome to RoPY - Roblox User Information Fetcher")
    print("Enter 'q' or 'quit' to exit the program")
    
    while True:
        try:
            user_input = input("\nEnter Roblox user ID: ").strip()
        except EOFError:
            print("\n\nInput stream ended. Exiting program. Goodbye!")
            sys.exit(0)
        
        # Check for quit commands (case-insensitive)
        if user_input.lower() in ('q', 'quit'):
            print("\nExiting program. Goodbye!")
            sys.exit(0)
            
        if validate_user_id(user_input):
            fetch_user_information(user_input)
            
            while True:
                try:
                    continue_choice = input("\nWould you like to look up another user? (y/n): ").strip().lower()
                    if continue_choice in ('y', 'yes'):
                        break
                    elif continue_choice in ('n', 'no'):
                        print("\nExiting program. Goodbye!")
                        sys.exit(0)
                    else:
                        print("Please enter 'y' or 'n'")
                except EOFError:
                    print("\n\nInput stream ended. Exiting program. Goodbye!")
                    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
