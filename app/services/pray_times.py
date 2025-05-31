import requests
from datetime import datetime

def get_prayer_times(region: str):
    url = f"https://api.aladhan.com/v1/timingsByCity?city={region}&country=Uzbekistan&method=2"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        timings = data['timings']
        date_readable = data['date']['readable']

        translated_timings = {
            "📅 Sana": date_readable,
            "\n🕋 Bomdod": timings["Fajr"],
            "🌄 Quyosh chiqishi": timings["Sunrise"],
            "☀️️ Peshin": timings["Dhuhr"],
            "🌤️ Asr": timings["Asr"],
            "🌇 Shom": timings["Maghrib"],
            "🌌 Hufton": timings["Isha"],
        }
        return translated_timings
    return None
