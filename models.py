from pydantic import BaseModel, ConfigDict

from datetime import date


class Author(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

class SchemaAuthor(Author):
    model_config = ConfigDict(from_attributes=True)

class Book(BaseModel):
    title: str
    author: SchemaAuthor
    description: str | None
    available_copies: int | None

class SchemaBook(Book):
   id: int
   model_config = ConfigDict(from_attributes=True)

class Borrow(BaseModel):
    book_id: int
    borrower_name: str
    borrow_date: date
    return_date: date

class SchemaBarrow(Borrow):
   id: int
   model_config = ConfigDict(from_attributes=True)
