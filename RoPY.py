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

def hent_brukerinformasjon(user_id: str) -> None:
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
        brukernavn = data.get("name", "Unknown")
        visningsnavn = data.get("displayName", "Unknown")
        opprettet_dato = data.get("created", "Unknown")
        avatar_url = data.get("avatarUrl", "Unknown")
        follower_count = data.get("followersCount", "Not available")
        friend_count = data.get("friendsCount", "Not available")

        # Clean up the created date
        rengjort_dato = parse_date(opprettet_dato)

        # Log successful API response
        logger.info(f"Successfully fetched data for user ID {user_id}")

        # Print user information
        print_user_info(brukernavn, visningsnavn, rengjort_dato, avatar_url, follower_count, friend_count)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        print("An error occurred while fetching user information. Please try again later.")
    except requests.exceptions.ConnectionError:
        logger.error("A network problem occurred while trying to fetch user information.")
        print("There was a network problem. Please check your connection and try again.")
    except requests.exceptions.Timeout:
        logger.error("The request timed out while trying to fetch user information.")
        print("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        print("An error occurred while fetching user information. Please try again later.")
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

def print_user_info(brukernavn: str, visningsnavn: str, rengjort_dato: str, avatar_url: str, follower_count: str, friend_count: str) -> None:
    """
    Displays information about a user.

    Parameters:
    brukernavn (str): The username of the user.
    visningsnavn (str): The display name of the user.
    rengjort_dato (str): The cleaned creation date of the user.
    avatar_url (str): The avatar URL of the user.
    follower_count (str): The follower count of the user.
    friend_count (str): The friend count of the user.
    """
    print("🕹️ User Information:")
    print(f"👤 Username: {brukernavn}")
    print(f"🧑‍🤝‍🧑 Display Name: {visningsnavn}")
    print(f"📅 Created: {rengjort_dato}")
    print(f"📸 Avatar URL: {avatar_url}")
    print(f"👥 Followers: {follower_count}")
    print(f"👫 Friends: {friend_count}")

def main() -> None:
    """
    Main function to run the script.
    Prompts the user to enter the name of a game and displays its information.
    """
    # Create a loop to handle input and stop the script after the user ID is provided
    while True:
        user_id = input("\nEnter Roblox user ID: ")
        if user_id.strip():  # Check if the ID is not empty
            if user_id.isdigit():  # Check if the ID is a valid number
                hent_brukerinformasjon(user_id)
                break  # Exit the loop when the ID is received
            else:
                print("Invalid ID, please try again.")
        else:
            print("ID cannot be empty, please try again.")

    # End the script
    print("\n🛑 Script has ended.")

if __name__ == "__main__":
    main()
