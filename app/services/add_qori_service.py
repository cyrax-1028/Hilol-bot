from app.database.database import async_session
from app.database.models import Qori

async def add_qori_to_db(name: str):
    async with async_session() as session:
        new_qori = Qori(name=name)
        session.add(new_qori)
        await session.commit()