from datetime import date

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional, List

from main import app

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
    available_copies = Column(Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Borrow(Base):
    __tablename__ = 'borrow'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    borrower_name = Column(String)
    borrow_date = Column(Date)
    return_date = Column(Date)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class AuthorIn(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

class AuthorOut(AuthorIn):
    id: int
    first_name: str
    last_name: str
    birth_date: date

class BookIn(BaseModel):
    title: str
    description: str
    author_id: int
    available_copies: int

class BookOut(BookIn):
    id: int
    title: str
    description: str
    author_id: int
    available_copies: int

class BorrowIn(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

class BorrowOut(BorrowIn):
    id: int
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

# Примеры эндпоинтов для авторов
@app.post("/authors", response_model=AuthorOut)
async def create_author(author: AuthorIn):
    # Логика создания автора
    return author

@app.get("/authors", response_model=List[AuthorOut])
async def get_authors():
    # Логика получения списка авторов
    return []

@app.get("/authors/{id}", response_model=AuthorOut)
async def get_author_by_id(id: int):
    # Логика получения информации об авторе по id
    return {"id": id, "first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01"}

# Добавьте эндпоинты для книг и выдач

# Пример запуска FastAPI приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)