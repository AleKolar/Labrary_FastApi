
from datetime import date
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import new_session, AuthorOrm, BookOrm, BorrowOrm
from models import SchemaAuthor, Book, Author, SchemaBook


class AuthorRepository:
    @classmethod
    async def create_author(cls, data: Author):
        async with new_session() as session:
            model = data.model_dump()
            existing_author = await cls.get_author_by_details(data=AuthorOrm(**model))

            if existing_author:
                return existing_author
            else:
                new_model = AuthorOrm(**model)
                session.add(new_model)
                await session.flush()
                await session.commit()
                return new_model

    @classmethod
    async def get_author_by_details(cls, data: AuthorOrm):
        async with new_session() as session:
            result = await session.execute(select(AuthorOrm).filter(
                (data.first_name == AuthorOrm.first_name) &
                (data.last_name == AuthorOrm.last_name) &
                (data.birth_date == AuthorOrm.birth_date)))

            author = result.scalars().first()
            return author

    @classmethod
    async def get_authors(cls) -> list[AuthorOrm]:
        async with new_session() as session:
            query = select(AuthorOrm)
            result = await session.execute(query)
            authors = result.scalars().all()
            return authors if authors else []

    @classmethod
    async def get_author_by_id(cls, id: int) -> AuthorOrm | None:
        async with new_session() as session:
            author = await session.get(AuthorOrm, id)
            return author if author else None


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
                await session.delete(author_to_delete)
                await session.commit()
                return author_to_delete
            return None


class BookRepository:
    @classmethod
    async def create_book(cls, book_data: Book):
        async with new_session() as session:
            data = book_data.model_dump()
            author_data = data['author']

            existing_author = await cls.get_existing_author(AuthorOrm(**author_data))

            if existing_author:
                author_id = existing_author.id
            else:
                new_author = AuthorOrm(**author_data)
                session.add(new_author)
                await session.flush()
                author_id = new_author.id

            query = await session.execute(
                select(BookOrm).filter(BookOrm.title == data['title'], BookOrm.author_id == author_id)
            )
            existing_book = query.scalars().first()

            if existing_book:
                existing_book.available_copies += 1
                await session.commit()
                return existing_book
            else:
                new_book_data = data.copy()
                new_book_data['available_copies'] = 1

                new_book = BookOrm(title=new_book_data['title'],
                                   description=new_book_data['description'],
                                   available_copies=new_book_data['available_copies'],
                                   author_id=author_id)

                session.add(new_book)
                await session.flush()
                await session.commit()

                return new_book


    @classmethod
    async def get_existing_author(cls, author_data):
        author = await AuthorRepository.get_author_by_details(author_data)
        return author

    @classmethod
    async def get_books(cls) -> List[SchemaBook]:
        async with new_session() as session:
            query = select(BookOrm).options(joinedload(BookOrm.author))
            result = await session.execute(query)
            books = result.scalars().all()

            schema_books = []
            for book in books:
                author_data = None
                if book.author:
                    author_data = {
                        'id': book.author.id,
                        'first_name': book.author.first_name,
                        'last_name': book.author.last_name,
                        'birth_date': book.author.birth_date.strftime('%Y-%m-%d') if book.author.birth_date else None
                    }

                schema_books.append(SchemaBook(
                    id=book.id,
                    title=book.title,
                    description=book.description,
                    available_copies=book.available_copies,
                    author=SchemaAuthor(**author_data) if author_data else None
                ))

            return schema_books

    @classmethod
    async def get_book_by_id(cls, id: int) -> SchemaBook | dict[str, None]:
        async with new_session() as session:
            query = select(BookOrm).where(BookOrm.id == id).options(joinedload(BookOrm.author))
            book_orm = await session.execute(query)
            book = book_orm.scalars().first()

            if book:
                author_data = None
                if book.author:
                    author_data = {
                        'id': book.author.id,
                        'first_name': book.author.first_name,
                        'last_name': book.author.last_name,
                        'birth_date': book.author.birth_date.strftime('%Y-%m-%d') if book.author.birth_date else None
                    }

                return SchemaBook(
                    id=book.id,
                    title=book.title,
                    description=book.description,
                    available_copies=book.available_copies,
                    author=SchemaAuthor(**author_data) if author_data else None
                )
            else:
                return None


    # @classmethod
    # async def update_book(cls, id: int, book: Book) -> Book:
    #     async with new_session() as session:
    #         stored_book = await session.get(BookOrm, id)
    #         if stored_book:
    #             # Обновление данных книги
    #             for key, value in book.model_dump().items():
    #                 if key not in ['author', 'available_copies']:
    #                     setattr(stored_book, key, value)
    #                     getattr(stored_book, 'available_copies')
    #
    #             # Проверяем наличие информации об авторе в книге
    #             if 'author' not in book.model_dump():
    #                 # Создаем нового автора на основе данных из словаря author_data
    #                 model = Author.model_dump(book.author)
    #                 new_author = AuthorOrm(**model)
    #                 session.add(new_author)
    #                 await session.commit()
    #
    #                 # Привязываем нового автора к книге
    #                 stored_book.author = new_author
    #             else:
    #                 # Обновляем автора книги, если он существует
    #                 author_id = book.model_dump().get('author')
    #                 if author_id:
    #                     author = await session.get(AuthorOrm, id)
    #                     if author:
    #                         stored_book.author = author
    #
    #             await session.commit()
    #
    #             return stored_book

    # @classmethod
    # async def update_book(cls, book_id: int, book_data: dict):
    #     async with new_session() as session:
    #         stored_book = await session.get(BookOrm, book_id)
    #         if stored_book:
    #             for key, value in book_data.items():
    #                 if key not in ['author', 'available_copies']:
    #                     if key in ['available_copies']:
    #                         getattr(stored_book, 'available_copies')
    #                     setattr(stored_book, key, value)
    #
    #             if 'author' in book_data:
    #                 author_data = book_data['author']
    #
    #                 if author_data:
    #                     new_author = AuthorOrm(**author_data)
    #                     session.add(new_author)
    #                     await session.flush()
    #
    #                     stored_book.author = new_author
    #
    #             await session.commit()
    #             return stored_book
    #         return None

    @classmethod
    async def update_book(cls, book_id: int, book_data: dict):
        async with new_session() as session:
            stored_book = await session.get(BookOrm, book_id)
            if stored_book:
                # Обновляем поля книги, кроме author и available_copies
                for key, value in book_data.items():
                    if key == 'author':
                        continue  # Пропускаем поле author, обрабатываем отдельно

                    setattr(stored_book, key, value)  # Обновляем другие поля

                if 'author' in book_data:
                    author_data = book_data['author']
                    if author_data:
                        existing_author = await session.get(AuthorOrm, author_data.get('id'))
                        if existing_author:
                            # Обновляем существующего автора
                            for attr, attr_value in author_data.items():
                                setattr(existing_author, attr, attr_value)
                            stored_book.author = existing_author
                        else:
                            # Создаем нового автора, если он не найден
                            new_author = AuthorOrm(**author_data)
                            session.add(new_author)
                            stored_book.author = new_author

                            # Обработка поля available_copies отдельно
                if 'available_copies' in book_data:
                    stored_book.available_copies = book_data['available_copies']  # Обновляем значение, если передано

                await session.commit()
                return stored_book
            return None



    @classmethod
    async def delete_book(cls, id: int) -> BookOrm:
        async with new_session() as session:
            book_to_delete = await session.get(BookOrm, id)
            if book_to_delete:
                await session.delete(book_to_delete)
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
            raise ValueError("Не все обязательные поля были предоставлены для создания borrow_data")

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


