from typing import Optional
from datetime import datetime

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class NewBook(BaseModel):
    id: Optional[int] = Field(description="not needed on creat", default=None)
    title:str = Field(min_length=1)
    author:str = Field(min_length=2)
    description:str = Field(min_length=1, max_length=100)
    rating:int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1990, lt=datetime.now().year + 1)

    model_config={
        'json_schema_extra':{
            "example":{
                "title": "Give your book a title",
                "author": "Write your name",
                "description": "Tell us about your boook",
                "rating": 5,
                "published_date":2000
            }
        }
    }


BOOKS = [
    Book(1, 'Pappu book', 'Pappu Yadav', 'for learning backchoodi', 5, 2005),
    Book(2, 'Gappu book', 'Gappu Yadav', 'for fun 1', 4, 2007),
    Book(3, 'Tappu book', 'Tappu Yadav', 'for fun 2', 2, 2001),
    Book(4, 'Lappu book', 'Lappu Yadav', 'for fun 3', 3, 2002),
    Book(5, 'book1', 'author 1', 'for fun 4', 4, 2001),
    Book(6, 'book2', 'author 2', 'for fun 5', 5, 2002)
]

@app.get('/books', status_code=status.HTTP_200_OK)
def get_book():
    return BOOKS

@app.get('/books/id/{book_id}', status_code=status.HTTP_200_OK)
def find_book_by_id(book_id: int=Path(gt=0)):
    book_to_return = []
    for book in BOOKS:
        if book.id == book_id:
            book_to_return.append(book)

    return book_to_return if len(book_to_return) > 0 else HTTPException(status_code=404, detail="Book not found")
    
@app.get('/books/rating/{book_rating}', status_code=status.HTTP_200_OK)
def book_by_rating(book_rating:int = Path(gt=-1, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)

    return book_to_return        

@app.get('/books/published_date/')
def book_by_year(published_date:int=Query(gt=1990, lt=datetime.now().year+1)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
def create_book(new_book : NewBook):
    convert_to_Book_type = Book(**new_book.model_dump())
    print(type(convert_to_Book_type))
    BOOKS.append(id_finder(convert_to_Book_type))

@app.put('/books/update-book', status_code=status.HTTP_204_NO_CONTENT)
def update_book(book:NewBook):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


def id_finder(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+1 
    return book



@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            return {"message":f"Book with book id {book_id} removed from the list"}
    return HTTPException(status_code=200, detail="Book not found")