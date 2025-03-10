import logging
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Developer mode flag ---
# For developers only: Set this to True to enable developer mode
DEVELOPER_MODE = False  # Set to True for extra technical details

# Constants
API_URL = "https://users.roblox.com/v1/users/"
LANGUAGE_EN = 'en'

def fetch_user_information(user_id: str) -> None:
    """
    Fetch data from the Roblox API and print user information.
    
    Parameters:
    user_id (str): The ID of the Roblox user.
    """
    url = f"{API_URL}{user_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        user_info = {
            "username": data.get("name", "Unknown"),
            "display_name": data.get("displayName", "Unknown"),
            "created_date": parse_date(data.get("created", "Unknown")),
            "avatar_url": data.get("avatarUrl", "Unknown"),
            "followers_count": data.get("followersCount", "Not available"),
            "friends_count": data.get("friendsCount", "Not available")
        }

        # Log successful API response
        logger.info(f"Successfully fetched data for user ID {user_id}. Data: {data}")

        # Print user information
        display_user_info(**user_info)

    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
            requests.exceptions.Timeout, requests.exceptions.RequestException) as req_err:
        logger.error(f"Request error occurred: {req_err}")
        print("A network or request error occurred while fetching user information. Please try again later.")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        print("An unexpected error occurred. Please try again later.")

def parse_date(date_str: str) -> str:
    """
    Parse and format the date string.
    
    Parameters:
    date_str (str): The date string to parse.
    
    Returns:
    str: The formatted date string.
    """
    date_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return date_str

def display_user_info(username: str, display_name: str, created_date: str, avatar_url: str, followers_count: str, friends_count: str) -> None:
    """
    Displays information about a user.
    
    Parameters:
    username (str): The username of the user.
    display_name (str): The display name of the user.
    created_date (str): The cleaned creation date of the user.
    avatar_url (str): The avatar URL of the user.
    followers_count (str): The follower count of the user.
    friends_count (str): The friend count of the user.
    """
    print("🕹️ User Information:")
    print(f"👤 Username: {username}")
    print(f"🧑‍🤝‍🧑 Display Name: {display_name}")
    print(f"📅 Created: {created_date}")
    print(f"📸 Avatar URL: {avatar_url}")
    print(f"👥 Followers: {followers_count}")
    print(f"👫 Friends: {friends_count}")

def main() -> None:
    """
    Main function to run the script.
    Prompts the user to enter the ID of a Roblox user and displays their information.
    """
    while True:
        user_id = input("\nEnter Roblox user ID: ")
        if user_id.strip() and user_id.isdigit():  # Check if the ID is not empty and is a valid number
            fetch_user_information(user_id)
            break  # Exit the loop when the ID is received
        else:
            print("Invalid ID, please enter a valid numeric user ID.")

    # End the script
    print("\n🛑 Script has ended.")

if __name__ == "__main__":
    main()