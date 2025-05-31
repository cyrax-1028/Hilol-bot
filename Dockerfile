# Python rasmiy image dan foydalanamiz
FROM python:3.11-slim

# Ishchi katalog
WORKDIR /app

# requirements.txt faylini konteynerga nusxalash
COPY requirements.txt .

# Virtual muhit yaratamiz va kutubxonalarni o'rnatamiz
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# Loyihaning qolgan fayllarini nusxalash
COPY . .

# PATH ga virtual muhitni qo'shish
ENV PATH="/opt/venv/bin:$PATH"

# Botni ishga tushirish komandasi (agar faylingiz boshqacha bo'lsa, main.py o‘rniga uni yozing)
CMD ["python", "main.py"]