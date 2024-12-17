from datetime import date

from sqlalchemy import Integer, Column, String, ForeignKey, Date
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

engine = create_async_engine("sqlite:///api_library.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[date]

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    available_copies: Mapped[int | None]

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Borrow(Base):
    __tablename__ = 'borrow'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    borrower_name: Mapped[str]
    borrow_date: Mapped[date]
    return_date: Mapped[date]

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


