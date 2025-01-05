from datetime import date
from typing import List

from sqlalchemy import select

from database import new_session, AuthorOrm, BookOrm, BorrowOrm

from models import Author, Book, SchemaBook


class AuthorRepository:
    @classmethod
    async def create_author(cls, data: AuthorOrm) -> int:
        async with new_session() as session:
            existing_author = await cls.get_author_by_details(data.first_name, data.last_name, data.birth_date)

            if existing_author:
                return existing_author.id
            else:
                session.add(data)
                await session.flush()
                await session.commit()
                return data.id

    @classmethod
    async def get_author_by_details(cls, first_name: str, last_name: str, birth_date: date) -> AuthorOrm:
        async with new_session() as session:
            result = await session.execute(select(AuthorOrm).filter(
                (AuthorOrm.first_name == first_name) &
                (AuthorOrm.last_name == last_name) &
                (AuthorOrm.birth_date == birth_date)
            ))
            author = result.scalars().first()
            return author

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
            if author_id is None:
                raise ValueError("Для создания книги необходимо указать Author_id")

            author = await AuthorRepository.get_author_by_id(author_id)

            if author is None:
                raise ValueError("Сначала создайте автора !")

            book = BookOrm(**book_data, author_id=author_id)
            session.add(book)
            await session.commit()

            return book.id

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
        borrower_name = borrow_data.get("borrower_name")
        author_id = borrow_data.get("author_id")
        book_id = borrow_data.get("book_id")

        if not borrower_name or not author_id or not book_id:
            raise ValueError("Не все обязательные поля были предоставлены для создания займа")

        async with new_session() as session:
            new_borrow = BorrowOrm(
                borrower_name=borrower_name,
                author_id=author_id,
                book_id=book_id
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


