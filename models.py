from pydantic import BaseModel

from datetime import date


class AuthorIn(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

class AuthorOut(AuthorIn):
    id: int

class BookIn(BaseModel):
    title: str
    description: str
    author_id: int
    available_copies: int

class BookOut(BookIn):
    id: int

class BorrowIn(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

class BorrowOut(BorrowIn):
    id: int

