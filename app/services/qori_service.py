from app.database.models import Qori
from app.database.database import async_session
from sqlalchemy import select


async def get_all_qorilar():
    async with async_session() as session:
        result = await session.execute(select(Qori))
        return result.scalars().all()

async def get_qori_by_id(qori_id: int):
    async with async_session() as session:
        return await session.get(Qori, qori_id)

async def add_qori(name: str):
    async with async_session() as session:
        new_qori = Qori(name=name)
        session.add(new_qori)
        await session.commit()
        return new_qori

async def update_qori(qori_id: int, new_name: str):
    async with async_session() as session:
        qori = await session.get(Qori, qori_id)
        if qori:
            qori.name = new_name
            await session.commit()
            return True
        return False

async def delete_qori(qori_id: int):
    async with async_session() as session:
        qori = await session.get(Qori, qori_id)
        if qori:
            await session.delete(qori)
            await session.commit()
            return True
        return False