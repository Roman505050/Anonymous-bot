from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, nullable=False, unique=True)
    is_looking: Mapped[bool] = mapped_column(nullable=False, default=False)
    chat_with: Mapped[int] = mapped_column(nullable=True)