from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from models import AuthorOut, AuthorIn, BookOut, BookIn, BorrowOut, BorrowIn



app = FastAPI()

# Эндпоинтs для авторов
authors = []

@app.post("/authors", response_model=AuthorOut)
async def create_author(author: AuthorIn):
    new_author = AuthorOut(id=len(authors) + 1, **author.dict())
    authors.append(new_author)
    return new_author

@app.get("/authors", response_model=List[AuthorOut])
async def get_authors():
    return authors

@app.get("/authors/{id}", response_model=AuthorOut)
async def get_author_by_id(id: int):
    for author in authors:
        if author.id == id:
            return author
    return {"error": "Author not found"}

@app.put("/authors/{id}", response_model=AuthorOut)
async def update_author(id: int, author: AuthorIn):
    for stored_author in authors:
        if stored_author.id == id:
            stored_author.first_name = author.first_name
            stored_author.last_name = author.last_name
            stored_author.birth_date = author.birth_date
            return stored_author
    return {"error": "Author not found"}

@app.delete("/authors/{id}", response_model=AuthorOut)
async def delete_author(id: int):
    for index, author in enumerate(authors):
        if author.id == id:
            deleted_author = authors.pop(index)
            return deleted_author
    return {"error": "Author not found"}


# Эндпоинтs для книг

books = []

@app.post("/books", response_model=BookOut)
async def create_book(book: BookIn):
    new_book = BookOut(id=len(books) + 1, **book.dict())
    books.append(new_book)
    return new_book

@app.get("/books", response_model=List[BookOut])
async def get_books():
    return books

@app.get("/books/{id}", response_model=BookOut)
async def get_book_by_id(id: int):
    for book in books:
        if book.id == id:
            return book
    return {"error": "Book not found"}

@app.put("/books/{id}", response_model=BookOut)
async def update_book(id: int, book: BookIn):
    for stored_book in books:
        if stored_book.id == id:
            stored_book.title = book.title
            stored_book.description = book.description
            stored_book.author_id = book.author_id
            stored_book.available_copies = book.available_copies
            return stored_book
    return {"error": "Book not found"}

@app.delete("/books/{id}", response_model=BookOut)
async def delete_book(id: int):
    for index, book in enumerate(books):
        if book.id == id:
            deleted_book = books.pop(index)
            return deleted_book
    return {"error": "Book not found"}


# Эндпоинтs для выдач

borrows = []

@app.post("/borrows", response_model=BorrowOut)
async def create_borrow(borrow: BorrowIn):
    new_borrow = BorrowOut(id=len(borrows) + 1, **borrow.dict())
    borrows.append(new_borrow)
    return new_borrow

@app.get("/borrows", response_model=List[BorrowOut])
async def get_borrows():
    return borrows

@app.get("/borrows/{id}", response_model=BorrowOut)
async def get_borrow_by_id(id: int):
    for borrow in borrows:
        if borrow.id == id:
            return borrow
    return {"error": "Borrow not found"}

@app.patch("/borrows/{id}/return", response_model=BorrowOut)
async def return_borrow(id: int, return_date: date):
    for borrow in borrows:
        if borrow.id == id:
            borrow.return_date = return_date
            return borrow
    return {"error": "Borrow not found"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Swagger UI")

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()


# Эапуск FastAPI приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
