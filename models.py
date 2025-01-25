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
    author: Optional[Author]
    description: Optional[str] = None
    available_copies: Optional[int] = None


class SchemaBook(Book):
    id: int
    model_config = ConfigDict(from_attributes=True)

    def dict(self, **kwargs):
        data = super(SchemaBook, self).model_dump(**kwargs)

        if data.get('author'):
            author_data = data['author']
            data['first_name'] = author_data.get('first_name')
            data['last_name'] = author_data.get('last_name')
            data['birth_date'] = author_data.get('birth_date')
            del data['author']

        return data


class Borrow(BaseModel):
    book_id: int
    author_id: Optional[int] = None
    borrower_name: str
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None

class SchemaBarrow(Borrow):
   id: int
   model_config = ConfigDict(from_attributes=True)


