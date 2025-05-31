from app.database.models import User
from app.database.database import async_session
from sqlalchemy.future import select

import logging

logger = logging.getLogger(__name__)


async def save_user_if_not_exists(tg_user):
    try:
        async with async_session() as session:
            result = await session.execute(select(User).where(User.user_id == tg_user.id))
            user = result.scalar_one_or_none()

            if not user:
                new_user = User(
                    user_id=tg_user.id,
                    first_name=tg_user.first_name,
                    last_name=tg_user.last_name,
                    username=tg_user.username,
                )
                session.add(new_user)
                await session.commit()
                logger.info(f"New user saved: {tg_user.id} - {tg_user.username}")
            else:
                logger.info(f"User already exists: {tg_user.id}")
    except Exception as e:
        logger.error(f"Error saving user {tg_user.id}: {e}")

