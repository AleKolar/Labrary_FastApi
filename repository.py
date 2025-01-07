from datetime import date
from typing import List, Optional

from sqlalchemy import select

from database import new_session, AuthorOrm, BookOrm, BorrowOrm

from models import Author, Book, SchemaBook, SchemaAuthor


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
    async def delete_author(cls, id: int) -> SchemaAuthor:
        async with new_session() as session:
            author_to_delete = await session.get(AuthorOrm, id)
            if author_to_delete:
                session.delete(author_to_delete)
                await session.commit()
                return author_to_delete
            return None


class BookRepository:
    @classmethod
    async def create_book(cls, book_data: dict) -> int:
        async with new_session() as session:
            if 'author' not in book_data or not book_data['author']:
                raise ValueError("Key 'author' is missing or empty in book_data")

            author_data = {
                'first_name': book_data['author']['first_name'],
                'last_name': book_data['author']['last_name'],
                'birth_date': book_data['author']['birth_date']
            }

            existing_author = await cls.get_existing_author(session, author_data)

            if existing_author:
                author_id = existing_author.id
            else:
                author_id = await AuthorRepository.create_author(AuthorOrm(**author_data))
                author_data['id'] = author_id

            book_data['author_id'] = author_id
            del book_data['author']

            book = BookOrm(**book_data)
            session.add(book)
            await session.commit()

            book.available_copies += 1
            session.add(book)
            await session.commit()

            return book.id
    @classmethod
    async def get_existing_author(cls, session, author_data: dict) -> Optional[AuthorOrm]:
        query = select(AuthorOrm).filter(
            (AuthorOrm.first_name == author_data['first_name']) &
            (AuthorOrm.last_name == author_data['last_name']) &
            (AuthorOrm.birth_date == author_data['birth_date'])
        )

        result = await session.execute(query)
        return result.first()

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

    @classmethod
    async def borrow_book(cls, book_id: int):
        async with new_session() as session:
            book = await session.get(BookOrm, book_id)
            if book:
                if book.available_copies > 0:
                    book.available_copies -= 1
                    await session.commit()

    @classmethod
    async def return_book(cls, book_id: int):
        async with new_session() as session:
            book = await session.get(BookOrm, book_id)
            if book:
                book.available_copies += 1
                await session.commit()

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


