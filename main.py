from contextlib import asynccontextmanager
from datetime import date
from typing import List, Dict

from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html

from database import create_tables, delete_tables, AuthorOrm
from models import Author, Book, Borrow, SchemaAuthor
from repository import AuthorRepository, BookRepository, BorrowRepository



@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")

app = FastAPI(lifespan=lifespan)


# Эндпоинтs для авторов

@app.post("/", response_model=Author)
async def create_author(author: Author) -> dict:
    author_orm = AuthorOrm(**author.dict())
    author_id = await AuthorRepository.create_author(author_orm)
    return {"author_id": author_id}

@app.get("/authors", response_model=List[Author])
async def get_authors():
    authors = await AuthorRepository.get_authors()
    return authors

@app.get("/authors/{id}", response_model=Author)
async def get_author_by_id(id: int):
    author = await AuthorRepository.get_author_by_id(id)
    if author:
        return author
    return {"error": "Author not found"}

@app.put("/authors/{id}", response_model=Author)
async def update_author_route(id: int, author: Author):
    updated_author = await AuthorRepository.update_author(id, author.dict())
    if updated_author:
        return updated_author
    return {"error": "Author not found"}

@app.delete("/authors/{id}", response_model=Author)
async def delete_author_route(id: int):
    deleted_author = await AuthorRepository.delete_author(id)
    if deleted_author:
        return deleted_author
    return {"error": "Author not found"}

# Эндпоинты для книг

@app.post("/books", response_model=Book)
async def create_book_route(book: Book):
    new_book = await BookRepository.create_book(book.dict())
    return new_book

@app.get("/books", response_model=List[Book])
async def get_books_route():
    books = await BookRepository.get_books()
    return books

@app.get("/books/{id}", response_model=Book)
async def get_book_by_id_route(id: int):
    book = await BookRepository.get_book_by_id(id)
    if book:
        return book
    return {"error": "Book not found"}

@app.put("/books/{id}", response_model=Book)
async def update_book_route(id: int, book: Book):
    updated_book = await BookRepository.update_book(id, book.dict())
    if updated_book:
        return updated_book
    return {"error": "Book not found"}

@app.delete("/books/{id}", response_model=Book)
async def delete_book_route(id: int):
    deleted_book = await BookRepository.delete_book(id)
    if deleted_book:
        return deleted_book
    return {"error": "Book not found"}


# Эндпоинтs для выдач

@app.post("/borrows", response_model=Borrow)
async def create_borrow_route(borrow: Borrow):
    new_borrow = await BorrowRepository.create_borrow(borrow.dict())
    return new_borrow

@app.get("/borrows", response_model=List[Borrow])
async def get_borrows_route():
    borrows = await BorrowRepository.get_borrows()
    return borrows

@app.get("/borrows/{id}", response_model=Borrow)
async def get_borrow_by_id_route(id: int):
    borrow = await BorrowRepository.get_borrow_by_id(id)
    if borrow:
        return borrow
    return {"error": "Borrow not found"}

@app.patch("/borrows/{id}/return", response_model=Borrow)
async def return_borrow_route(id: int, return_date: date):
    returned_borrow = await BorrowRepository.return_borrow(id, return_date)
    if returned_borrow:
        return returned_borrow
    return {"error": "Borrow not found"}

# @router.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Swagger UI")
#
# @router.get("/openapi.json", include_in_schema=False)
# async def get_open_api_endpoint():
#     return app.openapi()
#
#
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

