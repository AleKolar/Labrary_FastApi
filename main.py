from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html

from database import async_sessionmaker
from models import Author,Book,Borrow



app = FastAPI()

async def get_async_db():
    async_db = async_sessionmaker()
    try:
        yield async_db
    finally:
        await async_db.close()

# Эндпоинтs для авторов
authors = []

@app.post("/authors", response_model=Author)
async def create_author(author: Author, db = Depends(get_async_db)):
    async with async_sessionmaker() as session:
        db_author = Author(**author.dict())
        session.add(db_author)
        await session.commit()
        await session.refresh(db_author)
        return db_author

@app.get("/authors", response_model=List[Author])
async def get_authors(db = Depends(get_async_db)):
    async with async_sessionmaker() as session:
        authors = session.query(Author).all()
        return authors

@app.get("/authors/{id}", response_model=Author)
async def get_author_by_id(id: int, db = Depends(get_async_db)):
    async with db() as session:
        author = await session.get(Author, id)
        if author:
            return author
        return {"error": "Author not found"}

@app.put("/authors/{id}", response_model=Author)
async def update_author(id: int, author: Author, db = Depends(get_async_db)):
    async with db() as session:
        stored_author = await session.get(Author, id)
        if stored_author:
            for key, value in author.dict().items():
                setattr(stored_author, key, value)
            await session.commit()
            return stored_author
        return {"error": "Author not found"}

@app.delete("/authors/{id}", response_model=Author)
async def delete_author(id: int, db = Depends(get_async_db)):
    async with db() as session:
        author = await session.get(Author, id)
        if author:
            session.delete(author)
            await session.commit()
            return author
        return {"error": "Author not found"}

# Эндпоинты для книг

books = []

async def get_async_db():
    async_db = async_sessionmaker()
    try:
        yield async_db
    finally:
        await async_db.close()

@app.post("/books", response_model=Book)
async def create_book(book: Book, db = Depends(get_async_db)):
    async with db() as session:
        new_book = Book(id=len(books) + 1, **book.dict())
        books.append(new_book)
        return new_book

@app.get("/books", response_model=List[Book])
async def get_books(db = Depends(get_async_db)):
    async with db() as session:
        return books

@app.get("/books/{id}", response_model=Book)
async def get_book_by_id(id: int, db = Depends(get_async_db)):
    async with db() as session:
        for book in books:
            if book.id == id:
                return book
        return {"error": "Book not found"}

@app.put("/books/{id}", response_model=Book)
async def update_book(id: int, book: Book, db = Depends(get_async_db)):
    async with db() as session:
        for stored_book in books:
            if stored_book.id == id:
                stored_book.title = book.title
                stored_book.description = book.description
                stored_book.author_id = book.author_id
                stored_book.available_copies = book.available_copies
                return stored_book
        return {"error": "Book not found"}

@app.delete("/books/{id}", response_model=Book)
async def delete_book(id: int, db = Depends(get_async_db)):
    async with db() as session:
        for index, book in enumerate(books):
            if book.id == id:
                deleted_book = books.pop(index)
                return deleted_book
        return {"error": "Book not found"}


# Эндпоинтs для выдач

borrows = []

@app.post("/borrows", response_model=Borrow)
async def create_borrow(borrow: Borrow, db = Depends(get_async_db)):
    async with db() as session:
        new_borrow = Borrow(id=len(borrows) + 1, **borrow.dict())
        borrows.append(new_borrow)
        return new_borrow

@app.get("/borrows", response_model=List[Borrow])
async def get_borrows(db = Depends(get_async_db)):
    async with db() as session:
        return borrows

@app.get("/borrows/{id}", response_model=Borrow)
async def get_borrow_by_id(id: int, db = Depends(get_async_db)):
    async with db() as session:
        for borrow in borrows:
            if borrow.id == id:
                return borrow
        return {"error": "Borrow not found"}

@app.patch("/borrows/{id}/return", response_model=Borrow)
async def return_borrow(id: int, return_date: date, db = Depends(get_async_db)):
    async with db() as session:
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


# Запуск FastAPI приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
