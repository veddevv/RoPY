import requests
from datetime import datetime

# --- Developer mode flag ---
# For developers only: Set this to True to enable developer mode
DEVELOPER_MODE = False  # Set to True for extra technical details

def hent_brukerinformasjon(user_id, language):
    # Fetch data from the Roblox API
    url = f"https://users.roblox.com/v1/users/{user_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        brukernavn = data.get("name", "Unknown")
        visningsnavn = data.get("displayName", "Unknown")
        opprettet_dato = data.get("created", "Unknown")
        avatar_url = data.get("avatarUrl", "Unknown")
        follower_count = data.get("followersCount", "Not available" if language == 'en' else "Ikke tilgjengelig")
        friend_count = data.get("friendsCount", "Not available" if language == 'en' else "Ikke tilgjengelig")

        # Clean up the created date
        try:
            rengjort_dato = datetime.strptime(opprettet_dato, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            rengjort_dato = opprettet_dato

        # Print user information
        print_user_info(language, brukernavn, visningsnavn, rengjort_dato, avatar_url, follower_count, friend_count)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def print_user_info(language, brukernavn, visningsnavn, rengjort_dato, avatar_url, follower_count, friend_count):
    if language == 'en':
        print("🕹️ User Information:")
        print(f"👤 Username: {brukernavn}")
        print(f"🧑‍🤝‍🧑 Display Name: {visningsnavn}")
        print(f"📅 Created: {rengjort_dato}")
        print(f"📸 Avatar URL: {avatar_url}")
        print(f"👥 Followers: {follower_count}")
        print(f"👫 Friends: {friend_count}")
    else:
        print("🕹️ Brukerinformasjon:")
        print(f"👤 Brukernavn: {brukernavn}")
        print(f"🧑‍🤝‍🧑 Visningsnavn: {visningsnavn}")
        print(f"📅 Opprettet: {rengjort_dato}")
        print(f"📸 Avatar URL: {avatar_url}")
        print(f"👥 Følgere: {follower_count}")
        print(f"👫 Venner: {friend_count}")

def main():
    # Prompt the user to select a language
    language = ""
    while language not in ['en', 'no']:
        language = input("Choose language / Velg språk (en/no): ").lower()

    # Create a loop to handle input and stop the script after the user ID is provided
    while True:
        user_id = input("\nSkriv inn Roblox bruker-ID: " if language == 'no' else "\nEnter Roblox user ID: ")
        if user_id.strip():  # Check if the ID is not empty
            if user_id.isdigit():  # Check if the ID is a valid number
                hent_brukerinformasjon(user_id, language)
                break  # Exit the loop when the ID is received
            else:
                print("Ugyldig ID, prøv igjen." if language == 'no' else "Invalid ID, please try again.")
        else:
            print("ID kan ikke være tom, prøv igjen." if language == 'no' else "ID cannot be empty, please try again.")

    # End the script
    print("\n🛑 Skriptet er avsluttet." if language == 'no' else "\n🛑 Script has ended.")

if __name__ == "__main__":
    main()
