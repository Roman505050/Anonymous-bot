from sqlalchemy import select, update, ScalarResult
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs, AsyncEngine
from sqlalchemy.exc import NoResultFound

from .models import Base,Users

class DataBase:


    def __init__(self):
        self.engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///database/database.db")
        self.async_session: AsyncSession = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def create(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert(self, **kwargs) -> None:
        #підвердження транзакції запису даних в БД з словника **kwargs
        async with self.async_session.begin() as session:
            session.add(Users(**kwargs))

    async def user_update(self, user_id: int, **kwargs) -> None:
        stmt = (
            update(Users).
            where(Users.user_id == user_id).
            values(**kwargs)
        )
        
        async with self.async_session.begin() as session:
            await session.execute(stmt)

    async def get_users_looking_for_chat(self) -> list[int] | None: 
        stmt = select(Users.user_id).where(Users.is_looking == True)
        
        try:
            async with self.async_session.begin() as session:
                data = await session.execute(stmt)
                return [row[0] for row in data]  # Отримати перший стовпець (user_id) для кожного рядка
        except NoResultFound:
            return None

    async def get(self, user_id: int | None=None, all_data: bool=False) -> ScalarResult | None:
        stmt = (
            select(Users).
            where(Users.user_id == user_id)
        ) if user_id is not None else select(Users)

        try:
            async with self.async_session.begin() as session:
                data = await session.execute(stmt)
                return data.scalars().one() if not all_data else data.scalars().all()
        except NoResultFound:
            return None

    async def user_id_exists(self, user_id: int) -> bool: #запрос який вертає True|False взалежності чи є користувач в БД
        stmt = select(Users.user_id).where(Users.user_id == user_id)
        
        try:
            async with self.async_session.begin() as session:
                result = await session.execute(stmt)
                return bool(result.scalar_one_or_none())
        except NoResultFound:
            return False
