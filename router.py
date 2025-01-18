from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html


from main import app
from models import Book, Borrow, Author, SchemaAuthor, SchemaBook
from repository import AuthorRepository, BookRepository, BorrowRepository

router = APIRouter()
app.include_router(router)
@router.post("/", response_model=Author)
async def create_author_route(author: Author):
    author_id = await AuthorRepository.create_author(author)
    return {"author_id": author_id}

@router.get("/authors", response_model=List[Author])
async def get_authors_route():
    authors = await AuthorRepository.get_authors()
    return authors

@router.get("/authors/{id}", response_model=Author)
async def get_author_by_id_route(id: int):
    author = await AuthorRepository.get_author_by_id(id)
    if author:
        return author
    return {"error": "Author not found"}

@router.put("/authors/{id}", response_model=Author)
async def update_author_route(id: int, author: Author):
    updated_author = await AuthorRepository.update_author(id, author)
    if updated_author:
        return updated_author
    return {"error": "Author not found"}

@router.delete("/authors/{id}", response_model=SchemaAuthor)
async def delete_author_route(id: int):
    deleted_author = await AuthorRepository.delete_author(id)
    if deleted_author:
        return deleted_author
    raise HTTPException(status_code=404, detail="Author not found")

@router.post("/book", response_model=Book)
async def create_book_route(book: Book):
    book_data = book.model_dump()
    if 'author' not in book_data:
        raise ValueError("Key 'author' is missing in book_data")

    new_book = await BookRepository.create_book(book)
    return new_book

@router.get("/books", response_model=List[Book])
async def get_books_route():
    books = await BookRepository.get_books()
    return books

@router.get("/books/{id}", response_model=SchemaBook)
async def get_book_by_id_route(id: int):
    book = await BookRepository.get_book_by_id(id)
    if book:
        return book
    return {"error": "Book not found"}

@router.put("/books/{id}", response_model=SchemaBook, response_model_exclude={"author"})
async def update_book_route(id: int, book: Book):
    updated_book = await BookRepository.update_book(id, book)
    if updated_book:
        return updated_book
    return {"error": "Book not found"}

@router.delete("/books/{id}", response_model=SchemaBook)
async def delete_book_route(id: int):
    deleted_book = await BookRepository.delete_book(id)
    if deleted_book:
        return deleted_book
    return {"error": "Book not found"}

@router.post("/borrows", response_model=Borrow)
async def create_borrow_route(borrow: Borrow):
    new_borrow = await BorrowRepository.create_borrow(borrow)
    return new_borrow

@router.get("/borrows", response_model=List[Borrow])
async def get_borrows_route():
    borrows = await BorrowRepository.get_borrows()
    return borrows

@router.get("/borrows/{id}", response_model=Borrow)
async def get_borrow_by_id_route(id: int):
    borrow = await BorrowRepository.get_borrow_by_id(id)
    if borrow:
        return borrow
    return {"error": "Borrow not found"}

@router.patch("/borrows/{id}/return", response_model=Borrow)
async def return_borrow_route(id: int, return_date: date):
    returned_borrow = await BorrowRepository.return_borrow(id, return_date)
    if returned_borrow:
        return returned_borrow
    return {"error": "Borrow not found"}

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI Swagger UI")

@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()








