import requests

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
        brukernavn = data.get("name")
        visningsnavn = data.get("displayName")
        opprettet_dato = data.get("created")
        avatar_url = data.get("avatarUrl")
        follower_count = data.get("followersCount", "Not available" if language == 'en' else "Ikke tilgjengelig")
        friend_count = data.get("friendsCount", "Not available" if language == 'en' else "Ikke tilgjengelig")

        # Clean up the created date
        rengjort_dato = opprettet_dato.replace("T", " ").replace("Z", "")

        # Print user information based on selected language
        if language == 'en':
            print("🕹️ User Information:")
            print(f"👤 Username: {brukernavn}")
            print(f"🧑‍🤝‍🧑 Display Name: {visningsnavn}")
            print(f"📅 Created: {rengjort_dato}")
            print(f"👥 Followers: {follower_count}")
            print(f"🤝 Friends: {friend_count}")
            print(f"🖼️ Avatar: {avatar_url}")
        else:
            print("🕹️ Brukerinformasjon:")
            print(f"👤 Brukernavn: {brukernavn}")
            print(f"🧑‍🤝‍🧑 Visningsnavn: {visningsnavn}")
            print(f"📅 Opprettet: {rengjort_dato}")
            print(f"👥 Følgere: {follower_count}")
            print(f"🤝 Venner: {friend_count}")
            print(f"🖼️ Avatar: {avatar_url}")
        
        # Developer mode: Print additional debug information
        if DEVELOPER_MODE:
            print("\n🛠️ Developer Mode:")
            print(f"📡 Request URL: {url}")
            print(f"⌛ Status Code: {response.status_code}")
            print(f"📝 Full Response JSON: {data}")

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ {'HTTP error:' if language == 'en' else 'HTTP-feil:'} {http_err}")
    except requests.exceptions.ConnectionError:
        print(f"❌ {'Could not connect to Roblox API. Check your internet connection.' if language == 'en' else 'Kunne ikke koble til Roblox API. Sjekk internettforbindelsen.'}")
    except requests.exceptions.Timeout:
        print(f"❌ {'Request to Roblox API timed out.' if language == 'en' else 'Tidsavbrudd ved forespørsel til Roblox API.'}")
    except requests.exceptions.RequestException as err:
        print(f"❌ {'An error occurred:' if language == 'en' else 'En feil oppstod:'} {err}")
    except ValueError:
        print(f"❌ {'Unexpected response format from API.' if language == 'en' else 'Uventet svarformat fra API.'}")
    except Exception as e:
        print(f"❌ {'An unknown error occurred:' if language == 'en' else 'En ukjent feil oppstod:'} {e}")

# Prompt the user to select a language
language = ""
while language not in ['en', 'no']:
    language = input("Choose language / Velg språk (en/no): ").lower()

# Create a loop to handle input and stop the script after the user ID is provided
while True:
    user_id = input("\nSkriv inn Roblox bruker-ID: " if language == 'no' else "\nEnter Roblox user ID: ")
    if user_id.strip():  # Check if the ID is not empty
        hent_brukerinformasjon(user_id, language)
        break  # Exit the loop when the ID is received

# End the script
print("\n🛑 Skriptet er avsluttet." if language == 'no' else "\n🛑 Script has ended.")
