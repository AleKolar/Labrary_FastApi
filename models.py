from pydantic import BaseModel, ConfigDict

from datetime import date


class Author(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date

class SchemaAuthor(Author):
   id: int
   model_config = ConfigDict(from_attributes=True)

class Book(BaseModel):
    id: int
    title: str
    description: str | None
    author_id: int
    available_copies: int | None

class SchemaBook(Book):
   id: int
   model_config = ConfigDict(from_attributes=True)

class Borrow(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

class SchemaBarrow(Borrow):
   id: int
   model_config = ConfigDict(from_attributes=True)
