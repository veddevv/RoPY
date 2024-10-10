import requests

def get_roblox_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_data = response.json()
        return {
            "Username": user_data.get("name"),
            "Display Name": user_data.get("displayName"),
            "Description": user_data.get("description", "Ingen beskrivelse 😶"),
            "Creation Date": user_data.get("created"),
            "Is Banned": user_data.get("isBanned", False)  # Viser om brukeren er bannlyst
        }
    else:
        return f"❌ Error fetching data. Status code: {response.status_code}"

def get_roblox_user_followers(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("count", 0)
    else:
        return "❌ Kunne ikke hente følgere."

def get_roblox_user_following(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("count", 0)
    else:
        return "❌ Kunne ikke hente følgede."

def display_user_info(user_info, followers, following):
    if isinstance(user_info, dict):
        print(f"👤 Brukernavn: {user_info['Username']}")
        print(f"📛 Visningsnavn: {user_info['Display Name']}")
        print(f"📝 Beskrivelse: {user_info['Description']}")
        print(f"📅 Opprettet: {user_info['Creation Date']}")
        print(f"🚫 Bannlyst: {'Ja' if user_info['Is Banned'] else 'Nei'}")
        print(f"👥 Følgere: {followers}")
        print(f"🔗 Følger: {following}")
    else:
        print(user_info)

if __name__ == "__main__":
    # Be om bruker-ID fra brukeren
    user_id = input("Skriv inn Roblox-bruker-ID 🔍: ")

    # Hente og vise brukerinfo
    user_info = get_roblox_user_info(user_id)
    followers_count = get_roblox_user_followers(user_id)
    following_count = get_roblox_user_following(user_id)

    print("\n🔎 Hentet informasjon:")
    display_user_info(user_info, followers_count, following_count)
