import pytest
import asyncio
import datetime
from datetime import date
from unittest.mock import MagicMock, AsyncMock, patch

from sqlalchemy import select
from datetime import datetime

from database import AuthorOrm, new_session, BookOrm
from repository import BorrowRepository, BookRepository, AuthorRepository

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def new_db_session():
    async with new_session() as session:
        yield session

@pytest.fixture
def author_data():
    return {"first_name": "Test Author", "last_name": "Test Author"}

@pytest.fixture
def book_data():
    return {"title": "Test Book"}

@pytest.fixture
def borrow_data():
    return {"author_id": 1, "book_id": 1}

@pytest.fixture
def session_mock():
    return MagicMock()


@pytest.mark.asyncio
async def test_create_book_with_author(book_data, new_db_session, author_data):
    if 'birth_date' not in author_data or author_data['birth_date'] is None:
        author_data = {
            'first_name': author_data['first_name'],
            'last_name': author_data['last_name'],
            'birth_date': datetime.now()
        }

    author_orm = AuthorOrm(**author_data)
    author_id = await AuthorRepository.create_author(author_orm)
    assert author_id is not None

    book_data["author_id"] = author_id

    async for session in new_db_session:
        result = await session.execute(select(BookOrm).where(BookOrm.author_id == author_id))
        existing_books = result.fetchall()

        for existing_book in existing_books:
            await check_book(existing_book, author_id)

        book = await BookRepository.create_book(book_data)

    assert book is not None

async def check_book(existing_book, author_id):
    if existing_book.author_id == author_id:
        raise ValueError(f"Book with author_id {author_id} already exists in the database")


@pytest.mark.asyncio
async def test_create_book_without_existing_author(book_data, new_db_session, author_data):
    if 'birth_date' not in author_data or author_data['birth_date'] is None:
        author_data['birth_date'] = datetime.now()

        author_data = {
            'first_name': author_data['first_name'],
            'last_name': author_data['last_name'],
            'birth_date': datetime.now()
        }

    author_orm = AuthorOrm(**author_data)
    author_id = await AuthorRepository.create_author(author_orm)

    query = select(AuthorOrm).filter(
        (AuthorOrm.first_name == author_data['first_name']) &
        (AuthorOrm.last_name == author_data['last_name']) &
        (AuthorOrm.birth_date == author_data['birth_date'])
    )

    async for session in new_db_session:
        result = await session.execute(query)
        existing_author = result.first()

        if existing_author is None:
            with pytest.raises(ValueError) as e:
                await BookRepository.create_book(book_data, author_id=author_id)
            assert str(e.value) == "Сначала создайте автора !"
        else:
            book = await BookRepository.create_book(book_data,)
            return book


@pytest.mark.asyncio
async def delete_author(cls, id: int) -> AuthorOrm:
    async with new_session() as session:
        author_to_delete = await session.get(AuthorOrm, id)
        if author_to_delete:
            session.delete(author_to_delete)
            await session.commit()
            return author_to_delete
        return None

@pytest.mark.asyncio
async def test_get_authors(new_db_session):
    # Подготовка тестовых данных: создание нескольких записей авторов в базе данных
    author_data_1 = {"first_name": "John", "last_name": "Doe", "birth_date": date(1980, 1, 1)}
    author_data_2 = {"first_name": "Jane", "last_name": "Smith", "birth_date": date(1975, 5, 10)}

    author_orm_1 = AuthorOrm(**author_data_1)
    author_orm_2 = AuthorOrm(**author_data_2)

    await AuthorRepository.create_author(author_orm_1)
    await AuthorRepository.create_author(author_orm_2)

    # Вызов метода get_authors для получения списка авторов
    authors = await AuthorRepository.get_authors()

    # Проверка, что возвращенный результат является списком
    assert isinstance(authors, list)
    assert len(authors) > 0

@pytest.mark.asyncio
async def test_get_books(new_db_session):
    async with AsyncMock() as session:
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []

        session.execute = AsyncMock(return_value=mock_result)

        books = await BookRepository.get_books()
        assert isinstance(books, list)

@pytest.mark.asyncio
async def delete_book(cls, id: int) -> BookOrm:
    async with new_session() as session:
        book_to_delete = await session.get(BookOrm, id)
        if book_to_delete:
            session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        return None

@pytest.mark.asyncio
async def test_create_borrow(borrow_data, new_db_session):
    borrow = await BorrowRepository.create_borrow(borrow_data)
    assert borrow is not None

@pytest.mark.asyncio
async def test_get_borrows(new_db_session):
    borrows = await BorrowRepository.get_borrows()
    assert isinstance(borrows, list)

# pytest test_database.py