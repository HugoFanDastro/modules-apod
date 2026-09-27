import requests
import discord
from datetime import datetime
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
NASA_API_KEY = os.getenv("NASA_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_APOD")

def fetch_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erreur API NASA")

def send_to_discord(data):
    webhook = discord.SyncWebhook.from_url(DISCORD_WEBHOOK_URL)
    embed = discord.Embed(
        title=data["title"],
        description=data["explanation"],
        color=0x00ff00
    )
    embed.set_image(url=data["url"])
    embed.set_footer(text=f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    webhook.send(embed=embed)

if __name__ == "__main__":
    try:
        apod_data = fetch_apod()
        send_to_discord(apod_data)
        print("✅ Message envoyé à Discord !")
    except Exception as e:
        print(f"❌ Erreur : {e}")