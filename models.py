from datetime import date

from pydantic import BaseModel
from typing import Annotated

from sqlalchemy.orm import mapped_column, Mapped


uniq_str_an = Annotated[str, mapped_column(unique=True)]

class AuthorIn(BaseModel):
    first_name: str
    last_name: Mapped[uniq_str_an]
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
    borrower_name: Mapped[uniq_str_an]
    borrow_date: date
    return_date: date

class BorrowOut(BorrowIn):
    id: int

