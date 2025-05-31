import asyncio
import aiohttp
from app.database.database import async_session
from app.database.models import Surah

async def load_surahs_to_db():
    url = "https://api.alquran.cloud/v1/surah"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = (await response.json())["data"]

                async with async_session() as db:
                    async with db.begin():  # begin transaction
                        for item in data:
                            surah = Surah(
                                id=item["number"],
                                name=item["englishName"],
                                arabic_name=item["name"],
                                total_ayath=item["numberOfAyahs"],
                                revelation_type=item["revelationType"]
                            )
                            await db.merge(surah)  # async merge
                print("✅ 114 ta sura muvaffaqiyatli bazaga yuklandi.")
            else:
                print("❌ API'dan ma'lumot olishda xatolik:", response.status)

if __name__ == "__main__":
    asyncio.run(load_surahs_to_db())