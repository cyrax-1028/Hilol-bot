import asyncio
import google.generativeai as genai
from app.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

PERSONA_PROMPT = """
Sen Varkom kompaniyasi tomonidan yaratilgan sun’iy intellektisan.   
Har doim aqlli, samimiy va texnik bilimga ega bo‘lib javob berasan.   
Ammo diniy savollarga javob bermaysan va shu mavzulardan chetlanasan.   
Faqat texnik, kundalik hayot va boshqa umumiy mavzularda yordam berasan.   
Foydalanuvchi nima so‘rasa, muloyim va aniq tarzda javob ber.
"""


def contains_religious_keywords(text: str) -> bool:
    religious_keywords = [
        "quron", "namoz", "duo", "islam", "diniy", "namoz vaqti",
        "hijriy", "musulmon", "ro‘za", "hadis", "zakat", "haj",
        "islom", "ramazon", "alloh", "payg‘ambar"
    ]
    text_lower = text.lower()
    return any(word in text_lower for word in religious_keywords)


async def ask_bahromjon_ai(user_message: str) -> str:
    if contains_religious_keywords(user_message):
        return "Kechirasiz, diniy savollarga javob bera olmayman."

    prompt = f"{PERSONA_PROMPT}\nFoydalanuvchi: {user_message}\nBahromjon:"

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, model.generate_content, prompt)

    return response.text.strip()
