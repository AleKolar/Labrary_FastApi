import json

from models import Book, SchemaAuthor


def object_to_dict(obj):
    if isinstance(obj, Book):
        book_dict = obj.dict()
        if 'author' in book_dict:
            book_dict['author'] = object_to_dict(book_dict['author'])
        return book_dict
    return obj

def dict_to_object(obj_dict, obj_class):
    if obj_class == Book:
        if 'author' in obj_dict:
            obj_dict['author'] = dict_to_object(obj_dict['author'], SchemaAuthor)
        return obj_class(**obj_dict)
    return obj_class(**obj_dict)

