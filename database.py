from datetime import datetime, date
from typing import Annotated, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, relationship, mapped_column, declarative_base, DeclarativeBase, sessionmaker

from config import settings
from models import Author, Book, Borrow

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
   pass


class AuthorOrm(Model):
    __tablename__ = 'author'
    id: Mapped[int | None] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    birth_date: Mapped[datetime | None]

    book: Mapped["Book"] = relationship("BookOrm", back_populates="author", lazy='joined')
    borrows: Mapped["Borrow"] = relationship("BorrowOrm", back_populates="author", foreign_keys="[BorrowOrm.author_id]", lazy='joined')

    def model_dump(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None
        }



class BookOrm(Model):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str | None]
    available_copies: Mapped[int]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey('author.id'), nullable=True)

    borrows: Mapped["Borrow"] = relationship("BorrowOrm", back_populates="book", foreign_keys="[BorrowOrm.book_id]", lazy='joined')
    author: Mapped[Optional["AuthorOrm"]] = relationship("AuthorOrm", back_populates="book", lazy='joined')

    def model_dump(self):
        return {
            'title': self.title,
            'description': self.description,
            'author': self.author_id if self.author else None,
            'available_copies': self.available_copies,
        }

    # def book_dict(self):
    #     return {
    #         'title': self.title,
    #         'description': self.description,
    #         'available_copies': self.available_copies,
    #         'author': {
    #             'first_name': self.author.first_name if self.author else None,
    #             'last_name': self.author.last_name if self.author else None,
    #             'birth_date': self.author.birth_date.strftime('%Y-%m-%d') if self.author and self.author.birth_date else None
    #         }
    #     }


class BorrowOrm(Model):
    __tablename__ = 'borrow'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    borrower_name: Mapped[str]
    borrow_date: Mapped[date]
    return_date: Mapped[date]

    book: Mapped["BookOrm"] = relationship("BookOrm", back_populates="borrows", lazy='joined')
    author: Mapped["AuthorOrm"] = relationship("AuthorOrm", back_populates="borrows", lazy='joined')

    def model_dump(self):
        return {
            'book_id': self.book_id,
            'borrower_name': self.borrower_name,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date,
        }

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)

