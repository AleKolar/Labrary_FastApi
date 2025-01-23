from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Body
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.testing import exclude

from database import create_tables, delete_tables, BookOrm
from models import Author, Book, Borrow, SchemaAuthor, SchemaBook
from repository import AuthorRepository, BookRepository, BorrowRepository
from test_database import book_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)


# Эндпоинтs для авторов
@app.post("/")
async def create_author(author: Author = Depends()):
    author_repository = AuthorRepository()
    created_author = await author_repository.create_author(author)
    return {"message": "Автор успешно добавлен в библиотеку!", "author": created_author}


@app.get("/authors", response_model=List[Author])
async def get_authors():
    authors = await AuthorRepository.get_authors()
    return authors


@app.get("/authors/{id}", response_model=Author)
async def get_author_by_id(author_id: int):
    author = await AuthorRepository.get_author_by_id(author_id)
    if author:
        return author
    return {"error": "Author not found"}


@app.put("/authors/{id}", response_model=Author)
async def update_author(id: int, author: Author):
    updated_author = await AuthorRepository.update_author(id, author.model_dump())
    if updated_author:
        return updated_author
    return {"error": "Author not found"}


@app.delete("/authors/{id}", response_model=SchemaAuthor)
async def delete_author(id: int):
    deleted_author = await AuthorRepository.delete_author(id)
    if deleted_author:
        return deleted_author
    else:
        raise HTTPException(status_code=404, detail="Author not found")


# Эндпоинты для книг

@app.post("/book")
async def create_book(book_data: Book = Depends()):
    book = Book(**book_data.model_dump())
    book_repository = BookRepository()
    created_book = await book_repository.create_book(book)
    return {"message": "Книга успешно добавлена в библиотеку!", "book": created_book}


@app.get("/books", response_model=List[Book])
async def get_books():
    books = await BookRepository.get_books()
    return books


@app.get("/books/{id}", response_model=SchemaBook)
async def get_book_by_id(id: int):
    book = await BookRepository.get_book_by_id(id)
    if book:
        return book
    return {"error": "Book not found"}



@app.put("/books/{id}", response_model=SchemaBook)
async def update_book(book_id: int, book: Book = Depends()):
    book_data = book.model_dump()
    updated_book = await BookRepository.update_book(book_id, book_data)
    if updated_book:
        return updated_book
    return {"error": "Book not found"}



@app.delete("/books/{id}", response_model=SchemaBook)
async def delete_book(id: int):
    deleted_book = await BookRepository.delete_book(id)
    if deleted_book:
        return deleted_book
    return {"error": "Book not found"}


# Эндпоинтs для выдач

@app.post("/borrows", response_model=Borrow)
async def create_borrow(borrow: Borrow):
    new_borrow = await BorrowRepository.create_borrow(borrow.model_dump())
    return new_borrow


@app.get("/borrows", response_model=List[Borrow])
async def get_borrows():
    borrows = await BorrowRepository.get_borrows()
    return borrows


@app.get("/borrows/{id}", response_model=Borrow)
async def get_borrow_by_id(id: int):
    borrow = await BorrowRepository.get_borrow_by_id(id)
    if borrow:
        return borrow
    return {"error": "Borrow not found"}


@app.patch("/borrows/{id}/return", response_model=Borrow)
async def return_borrow(id: int, return_date: date):
    returned_borrow = await BorrowRepository.return_borrow(id, return_date)
    if returned_borrow:
        return returned_borrow
    return {"error": "Borrow not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
