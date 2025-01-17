from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class Author(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None

class SchemaAuthor(Author):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Book(BaseModel):
    title: str
    author: Author
    description: Optional[str] = None
    available_copies: Optional[int] = None


class SchemaBook(Book):
    id: int
    author: Optional[SchemaAuthor] = None
    model_config = ConfigDict(from_attributes=True)


class Borrow(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

class SchemaBarrow(Borrow):
   id: int
   model_config = ConfigDict(from_attributes=True)
