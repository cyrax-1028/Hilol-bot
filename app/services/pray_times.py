from datetime import datetime
from app.data.namaz import namoz_vaqtlari


def get_prayer_times(region: str, date_str: str = None):
    data = namoz_vaqtlari.namoz_vaqtlari

    if region not in data:
        return None

    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    if date_str not in data[region]:
        return None

    timings = data[region][date_str]

    translated_timings = {
        "📅 Sana": date_str,
        "🕋 Bomdod": timings.get("Bomdod"),
        "☀️️ Peshin": timings.get("Peshin"),
        "🌤️ Asr": timings.get("Asr"),
        "🌇 Shom": timings.get("Shom"),
        "🌌 Xufton": timings.get("Xufton"),
    }
    return translated_timings
