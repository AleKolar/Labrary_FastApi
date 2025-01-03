from datetime import datetime, date
from typing import Annotated

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, relationship, mapped_column, declarative_base

from config import settings
from models import Author, Book, Borrow

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

birth_date = Annotated[datetime, mapped_column(server_default=func.now())]

class AuthorOrm(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[birth_date]

    book: Mapped["Book"] = relationship("BookOrm", back_populates="author")
    borrows: Mapped["Borrow"] = relationship("BorrowOrm", back_populates="author", foreign_keys="[BorrowOrm.author_id]")

    def model_dump(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


class BookOrm(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    available_copies: Mapped[int | None]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))

    borrows: Mapped["Borrow"] = relationship("BorrowOrm", back_populates="book")
    author: Mapped["Author"] = relationship("AuthorOrm", back_populates="book")

    def model_dump(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author_id': self.author_id,
            'available_copies': self.available_copies,
        }

class BorrowOrm(Base):
    __tablename__ = 'borrow'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    borrower_name: Mapped[str]
    borrow_date: Mapped[date]
    return_date: Mapped[date]

    book: Mapped["BookOrm"] = relationship("BookOrm", back_populates="borrows")
    author: Mapped["AuthorOrm"] = relationship("AuthorOrm", back_populates="borrows")

    def model_dump(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'borrower_name': self.borrower_name,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date,
        }

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)




