import requests
from datetime import datetime
from typing import Optional, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Developer mode flag ---
# For developers only: Set this to True to enable developer mode
DEVELOPER_MODE = False  # Set to True for extra technical details

# Constants
API_URL = "https://users.roblox.com/v1/users/"
LANGUAGE_EN = 'en'
LANGUAGE_NO = 'no'

def hent_brukerinformasjon(user_id: str, language: str) -> None:
    """
    Fetch data from the Roblox API and print user information.

    Parameters:
    user_id (str): The ID of the Roblox user.
    language (str): The language for user information display.
    """
    url = f"{API_URL}{user_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        brukernavn = data.get("name", "Unknown")
        visningsnavn = data.get("displayName", "Unknown")
        opprettet_dato = data.get("created", "Unknown")
        avatar_url = data.get("avatarUrl", "Unknown")
        follower_count = data.get("followersCount", "Not available" if language == LANGUAGE_EN else "Ikke tilgjengelig")
        friend_count = data.get("friendsCount", "Not available" if language == LANGUAGE_EN else "Ikke tilgjengelig")

        # Clean up the created date
        rengjort_dato = parse_date(opprettet_dato)

        # Print user information
        print_user_info(language, brukernavn, visningsnavn, rengjort_dato, avatar_url, follower_count, friend_count)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        logger.error("A network problem occurred while trying to fetch user information.")
    except requests.exceptions.Timeout:
        logger.error("The request timed out while trying to fetch user information.")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")

def parse_date(date_str: str) -> str:
    """
    Parse and format the date string.

    Parameters:
    date_str (str): The date string to parse.

    Returns:
    str: The formatted date string.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return date_str

def print_user_info(language: str, brukernavn: str, visningsnavn: str, rengjort_dato: str, avatar_url: str, follower_count: str, friend_count: str) -> None:
    """
    Displays information about a user in the specified language.

    Parameters:
    language (str): The language for user information display.
    brukernavn (str): The username of the user.
    visningsnavn (str): The display name of the user.
    rengjort_dato (str): The cleaned creation date of the user.
    avatar_url (str): The avatar URL of the user.
    follower_count (str): The follower count of the user.
    friend_count (str): The friend count of the user.
    """
    info = {
        LANGUAGE_EN: {
            "title": "🕹️ User Information:",
            "username": "👤 Username: ",
            "display_name": "🧑‍🤝‍🧑 Display Name: ",
            "created": "📅 Created: ",
            "avatar_url": "📸 Avatar URL: ",
            "followers": "👥 Followers: ",
            "friends": "👫 Friends: "
        },
        LANGUAGE_NO: {
            "title": "🕹️ Brukerinformasjon:",
            "username": "👤 Brukernavn: ",
            "display_name": "🧑‍🤝‍🧑 Visningsnavn: ",
            "created": "📅 Opprettet: ",
            "avatar_url": "📸 Avatar URL: ",
            "followers": "👥 Følgere: ",
            "friends": "👫 Venner: "
        }
    }

    lang_info = info.get(language, info[LANGUAGE_EN])
    logger.info(f"{lang_info['title']}")
    logger.info(f"{lang_info['username']}{brukernavn}")
    logger.info(f"{lang_info['display_name']}{visningsnavn}")
    logger.info(f"{lang_info['created']}{rengjort_dato}")
    logger.info(f"{lang_info['avatar_url']}{avatar_url}")
    logger.info(f"{lang_info['followers']}{follower_count}")
    logger.info(f"{lang_info['friends']}{friend_count}")

def main() -> None:
    """
    Main function to run the script.
    Prompts the user to enter the name of a game and displays its information.
    """
    # Prompt the user to select a language
    language = ""
    while language not in [LANGUAGE_EN, LANGUAGE_NO]:
        language = input("Choose language / Velg språk (en/no): ").lower()

    # Create a loop to handle input and stop the script after the user ID is provided
    while True:
        user_id = input("\nSkriv inn Roblox bruker-ID: " if language == LANGUAGE_NO else "\nEnter Roblox user ID: ")
        if user_id.strip():  # Check if the ID is not empty
            if user_id.isdigit():  # Check if the ID is a valid number
                hent_brukerinformasjon(user_id, language)
                break  # Exit the loop when the ID is received
            else:
                logger.warning("Ugyldig ID, prøv igjen." if language == LANGUAGE_NO else "Invalid ID, please try again.")
        else:
            logger.warning("ID kan ikke være tom, prøv igjen." if language == LANGUAGE_NO else "ID cannot be empty, please try again.")

    # End the script
    logger.info("\n🛑 Skriptet er avsluttet." if language == LANGUAGE_NO else "\n🛑 Script has ended.")

if __name__ == "__main__":
    main()
