from sqlalchemy import create_async_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)

async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    book = relationship(
        "Book",
        back_populates="author",
        uselist=False,
        lazy="joined"
    )

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
    available_copies = Column(Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    author = relationship(
        "Author",
        back_populates="book",
        uselist=False
    )

class Borrow(Base):
    __tablename__ = 'borrow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    borrower_name = Column(String)
    borrow_date = Column(Date)
    return_date = Column(Date)

    book = relationship("Book", back_populates="borrows")
    author = relationship("Author", back_populates="borrows")

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


