import requests
import threading
import time

def hent_brukerinformasjon(user_id):
    # Hent data fra Roblox API
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
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
    else:
        print("❌ Fant ikke bruker. Sjekk ID-en og prøv igjen.")

def timeout():
    for i in range(20):  # 20 sekunders timer
        time.sleep(1)
        if i == 10:  # Etter 10 sekunder, spør om brukeren fortsatt er der
            print("\n🤔 Er du fortsatt der? Vennligst skriv inn ID-en!")
    
    print("\n⏰ Tidsgrensen ble nådd! Skriptet avbrytes.")
    exit()

# Start tidsavbruddet i en egen tråd
t = threading.Thread(target=timeout)
t.start()

# Kjør funksjonen med en ID
user_id = input("Skriv inn Roblox bruker-ID: ")

# Stop tidsavbruddet hvis input er mottatt
t.join(timeout=0)  # Hvis input mottas, stopper vi tidsavbruddet
hent_brukerinformasjon(user_id)
