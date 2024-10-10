import requests
import threading
import time
import sys

def hent_brukerinformasjon(user_id):
    # Hent data fra Roblox API
    url = f"https://users.roblox.com/v1/users/{user_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        data = response.json()
        brukernavn = data.get("name")
        visningsnavn = data.get("displayName")
        opprettet_dato = data.get("created")
        avatar_url = data.get("avatarUrl")
        follower_count = data.get("followersCount", "Ikke tilgjengelig")
        friend_count = data.get("friendsCount", "Ikke tilgjengelig")

        # Rengjør opprettet dato
        rengjort_dato = opprettet_dato.replace("T", " ").replace("Z", "")

        # Skriv ut informasjon med emojis
        print("🕹️ Brukerinformasjon:")
        print(f"👤 Brukernavn: {brukernavn}")
        print(f"🧑‍🤝‍🧑 Visningsnavn: {visningsnavn}")
        print(f"📅 Opprettet: {rengjort_dato}")
        print(f"👥 Følgere: {follower_count}")
        print(f"🤝 Venner: {friend_count}")
        print(f"🖼️ Avatar: {avatar_url}")

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP-feil: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Kunne ikke koble til Roblox API. Sjekk internettforbindelsen.")
    except requests.exceptions.Timeout:
        print("❌ Tidsavbrudd ved forespørsel til Roblox API.")
    except requests.exceptions.RequestException as err:
        print(f"❌ En feil oppstod: {err}")
    except ValueError:
        print("❌ Uventet svarformat fra API.")
    except Exception as e:
        print(f"❌ En ukjent feil oppstod: {e}")

def timeout(last_input_time):
    reminder_shown = False  # Flag to track if reminder has been shown
    while True:  # Kjør kontinuerlig
        time.sleep(1)
        current_time = time.time()
        time_left = 20 - (current_time - last_input_time[0])  # Calculate remaining time

        # Vis nedtellingstimer
        print(f"\r⏳ Tid igjen til inaktivitet: {max(0, int(time_left))} sekunder", end="")

        # Sjekk om det har gått mer enn 20 sekunder uten input
        if time_left <= 0:
            print("\n⏰ Tidsgrensen ble nådd! Skriptet avbrytes.")
            sys.exit()
        # Sjekk om det har gått mer enn 10 sekunder uten input
        elif time_left <= 10 and not reminder_shown:
            print("\n🤔 Er du fortsatt der? Vennligst skriv inn ID-en!")
            reminder_shown = True  # Set flag to True after showing the reminder

# Liste for å spore tiden for siste input
last_input_time = [time.time()]

# Start tidsavbruddet i en egen tråd
t = threading.Thread(target=timeout, args=(last_input_time,))
t.start()

# Kjør funksjonen med en ID
user_id = input("\nSkriv inn Roblox bruker-ID: ")
last_input_time[0] = time.time()  # Oppdater tiden for siste input

# Stop tidsavbruddet hvis input er mottatt
t.join(timeout=0)  # Hvis input mottas, stopper vi tidsavbruddet
hent_brukerinformasjon(user_id)
