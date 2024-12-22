from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, relationship, mapped_column, declarative_base

from config import settings
from models import Author, Book

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

int_pk = Annotated[int, mapped_column(primary_key=True)]
borrow_date = Annotated[datetime, mapped_column(server_default=func.now())]
return_date = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
birth_date = Annotated[datetime, mapped_column(server_default=func.now())]

class AuthorOrm(Base):
    __tablename__ = 'author'
    id: Mapped[int_pk] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[birth_date]

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="author",
        uselist=False,
        lazy="joined"
    )

class BookOrm(Base):
    __tablename__ = 'book'
    id: Mapped[int_pk] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    available_copies: Mapped[int | None]

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="book",
        uselist=False
    )

class BorrowOrm(Base):
    __tablename__ = 'borrow'
    id: Mapped[int_pk] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    borrower_name: Mapped[str]
    borrow_date: Mapped[borrow_date]
    return_date: Mapped[return_date]

    book:  Mapped["Book"] = relationship("Book", back_populates="borrows")
    author: Mapped["Author"] = relationship("Author", back_populates="borrows")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)




