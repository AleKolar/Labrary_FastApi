from unittest.mock import MagicMock, AsyncMock

import pytest
import asyncio

from database import AuthorOrm, new_session
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
    author_orm = AuthorOrm(**author_data)
    author_id = await AuthorRepository.create_author(author_orm)
    assert author_id is not None
    book_data["author_id"] = author_id
    try:
        book = await BookRepository.create_book(book_data, author_id)
    except TypeError as e:
        assert False, f"Error: {e}"
    assert book is not None

@pytest.mark.asyncio
async def test_create_book_without_author_id(book_data, new_db_session):
    with pytest.raises(ValueError) as e:
        await BookRepository.create_book(book_data, author_id=None)
    assert "Author_id must be provided to create a book." in str(e.value)


@pytest.mark.asyncio
async def test_get_authors(new_db_session):
    authors = await AuthorRepository.get_authors()
    assert isinstance(authors, list)


@pytest.mark.asyncio
async def test_delete_author(new_db_session, author_data):
    author_orm = AuthorOrm(**author_data)
    await AuthorRepository.create_author(author_orm)

    authors_before_deletion = await AuthorRepository.get_authors()
    author_id = authors_before_deletion[0].id

    deleted_author = await AuthorRepository.delete_author(author_id)

    assert deleted_author is not None

    authors_after_deletion = await AuthorRepository.get_authors()
    assert len(authors_after_deletion) == len(authors_before_deletion)
    assert deleted_author not in authors_after_deletion

@pytest.mark.asyncio
async def test_get_books(new_db_session):
    async with AsyncMock() as session:
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []

        session.execute = AsyncMock(return_value=mock_result)

        books = await BookRepository.get_books()
        assert isinstance(books, list)

@pytest.mark.asyncio
async def test_delete_book(new_db_session, book_data):
    book_data["author_id"] = 1
    book_id = await BookRepository.create_book(book_data, author_id=1)

    books_before_deletion = await BookRepository.get_books()

    deleted_book = await BookRepository.delete_book(book_id)

    assert deleted_book is not None

    books_after_deletion = await BookRepository.get_books()
    assert len(books_after_deletion) == len(books_before_deletion)
    assert deleted_book not in books_after_deletion

@pytest.mark.asyncio
async def test_create_borrow(borrow_data, new_db_session):
    borrow = await BorrowRepository.create_borrow(borrow_data)
    assert borrow is not None

@pytest.mark.asyncio
async def test_get_borrows(new_db_session):
    borrows = await BorrowRepository.get_borrows()
    assert isinstance(borrows, list)

# pytest test_database.py