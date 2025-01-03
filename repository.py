from datetime import date
from typing import List

from sqlalchemy import select

from database import new_session, AuthorOrm, BookOrm, BorrowOrm

from models import Author, Book, SchemaBook


class AuthorRepository:
    @classmethod
    async def create_author(cls, data: AuthorOrm) -> int:
        async with new_session() as session:
            session.add(data)
            await session.flush()
            await session.commit()
            return data.id

    @classmethod
    async def get_authors(cls) -> list[AuthorOrm]:
        async with new_session() as session:
            query = select(AuthorOrm)
            result = await session.execute(query)
            authors = result.scalars().all()
            return authors

    @classmethod
    async def get_author_by_id(cls, id: int) -> AuthorOrm:
        async with new_session() as session:
            author = await session.get(AuthorOrm, id)
            return author

    @classmethod
    async def update_author(cls, id: int, author_data: dict) -> AuthorOrm:
        async with new_session() as session:
            stored_author = await session.get(AuthorOrm, id)
            if stored_author:
                for key, value in author_data.items():
                    setattr(stored_author, key, value)
                await session.commit()
                return stored_author
            return None

    @classmethod
    async def delete_author(cls, id: int) -> AuthorOrm:
        async with new_session() as session:
            author_to_delete = await session.get(AuthorOrm, id)
            if author_to_delete:
                session.delete(author_to_delete)
                await session.commit()
                return author_to_delete
            return None

class BookRepository:
    @classmethod
    async def create_book(cls, book_data: dict, author_id: int = None) -> int:
        async with new_session() as session:
            new_book = BookOrm(**book_data)
            if author_id is not None:
                new_book.author_id = author_id
            else:
                raise ValueError("Author_id must be provided to create a book.")
            session.add(new_book)
            await session.flush()
            await session.commit()
            return new_book.id

    @classmethod
    async def get_books(cls) -> List[BookOrm]:
        async with new_session() as session:
            query = select(BookOrm)
            result = await session.execute(query)
            books = result.scalars().all()
            return books

    @classmethod
    async def get_book_by_id(cls, id: int) -> BookOrm:
        async with new_session() as session:
            book = await session.get(BookOrm, id)
            return book

    @classmethod
    async def update_book(cls, id: int, book_data: dict) -> BookOrm:
        async with new_session() as session:
            stored_book = await session.get(BookOrm, id)
            if stored_book:
                for key, value in book_data.items():
                    setattr(stored_book, key, value)
                await session.commit()
                return stored_book
            return None

    @classmethod
    async def delete_book(cls, id: int) -> BookOrm:
        async with new_session() as session:
            book_to_delete = await session.get(BookOrm, id)
            if book_to_delete:
                session.delete(book_to_delete)
                await session.commit()
                return book_to_delete
            return None

class BorrowRepository:
    @classmethod
    async def create_borrow(cls, borrow_data: dict) -> BorrowOrm:
        async with new_session() as session:
            new_borrow = BorrowOrm(
                borrower_name=borrow_data.get("borrower_name"),
                author_id=borrow_data.get("author_id"),
                book_id=borrow_data.get("book_id")
            )
            session.add(new_borrow)
            await session.commit()
            return new_borrow

    @classmethod
    async def get_borrows(cls) -> List[BorrowOrm]:
        async with new_session() as session:
            query = select(BorrowOrm)
            result = await session.execute(query)
            borrows = result.scalars().all()
            return borrows

    @classmethod
    async def get_borrow_by_id(cls, id: int) -> BorrowOrm:
        async with new_session() as session:
            borrow = await session.get(BorrowOrm, id)
            return borrow

    @classmethod
    async def return_borrow(cls, id: int, return_date: date) -> BorrowOrm:
        async with new_session() as session:
            borrow_to_return = await session.get(BorrowOrm, id)
            if borrow_to_return:
                borrow_to_return.return_date = return_date
                await session.commit()
                return borrow_to_return
            return None


