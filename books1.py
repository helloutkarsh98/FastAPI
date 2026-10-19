from fastapi import FastAPI

from fastapi import Body

ppa = FastAPI()

BOOKS = [
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "category": "Finance"},
    {"title": "Deep Work", "author": "Cal Newport", "category": "Productivity"},
    
    {"title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"title": "Ikigai", "author": "Hector Garcia", "category": "Self-Help"},
    {"title": "The Psychology of Money", "author": "Morgan Housel", "category": "Finance"},
    {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "category": "Fantasy"},
    {"title": "The Lean Startup", "author": "Eric Ries", "category": "Business"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "History"},
    {"title": "Deep Work", "author": "Cal Newport", "category": "Productivity"}
]

@ppa.get('/')
def first_api():
    return {
        'message': 'Hello World!',
        'status': 200
    }

@ppa.get('/books')
def get_all_books():
    return BOOKS


@ppa.get('/book/{dynamic_parameter}')
def get_parameter(dynamic_parameter):
    return get_book_by_parameter(dynamic_parameter)
    


@ppa.get('/books/{book_name}')
def get_book_by_parameter(book_name: str):
    for book in BOOKS:
        if book['title'].lower() == book_name.lower():
            return book
    return {"message" : "Book not found", "status": 404}


@ppa.get('/books/')
def get_book_by_query(category_name:str):
    books_to_return=[]
    for book in BOOKS:
        if book['category'].casefold() == category_name.casefold():
            books_to_return.append(book)
    return books_to_return     
   

@ppa.get('/books/{book_name}/')
def get_book_by_param_and_query(book_name:str, category_name:str):
    books_to_return = []
    for book in BOOKS:
        if book['title'].casefold() == book_name.casefold() and book['category'].casefold() == category_name.casefold():
            books_to_return.append(book)

    if len(books_to_return) > 0:
        return books_to_return
    else :
        return {"message" : "Book not found", "status": 404}


@ppa.get('/books/author/{author}')
def get_book_by_author(author:str):
    books_to_return=[]
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return books_to_return
    else:
        return {"message" : f"Book by {author} not found"}



#POST request
@ppa.post('/books/new_book')
def insert_book(new_book = Body(...)):
    BOOKS.append(new_book)
    return {
        'message': 'Book inserted successfully!',
        'status': 200
    }


#PUT request
@ppa.put('/books/update_book')
def update_book(book_name:str, update_book = Body(...)):
    flag = False
    for book in BOOKS:
        if book['title'].casefold() == book_name.casefold():
            flag = True
            book['title'] = update_book['title']
            book['author'] = update_book['author']
            book['category'] = update_book['category']

    if not flag:
        return{"message": f"{book_name} book not found"}
    else:
        return {"message" : f"{book_name} book updated successfully!"}


#DELETE request
@ppa.delete('/books/delete_book/{book_name}')
def delete_book(book_name : str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_name.casefold():
            del BOOKS[i]
            return {"message" : f"{book_name} book deleted successfully!"}
    return {"message" : f"{book_name} book not found"}


