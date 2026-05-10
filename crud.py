from fastapi import FastAPI,status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


books = [
    {
        "id": 1,
        "title": "Cien años de soledad",
        "author": "Gabriel García Márquez",
        "publish_date": "1967-05-30"
    },
    {
        "id": 2,
        "title": "El señor de los anillos",
        "author": "J.R.R. Tolkien",
        "publish_date": "1954-07-29"
    },
    {
        "id": 3,
        "title": "Harry Potter y la piedra filosofal",
        "author": "J.K. Rowling",
        "publish_date": "1997-06-26"
    },
    {
        "id": 4,
        "title": "1984",
        "author": "George Orwell",
        "publish_date": "1949-06-08"
    },
    {
        "id": 5,
        "title": "El principito",
        "author": "Antoine de Saint-Exupéry",
        "publish_date": "1943-04-06"
    },
]


app = FastAPI()

@app.get("/book")
def get_book():
    return books

@app.get("/book/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Page Not Found')

class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str


@app.post("/book")
def create_book(book:Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_date: str

@app.put("/book/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update.title
            book['author'] = book_update.author
            book['publish_date'] = book_update.publish_date
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")


@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book) 
            return{"message" : "Our Book Deleted"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Deleted")
