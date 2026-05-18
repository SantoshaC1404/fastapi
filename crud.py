from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1, 
        "title": "The Great Gatsby", 
        "author": "F. Scott Fitzgerald"
    },
    {
        "id": 2, 
        "title": "To Kill a Mockingbird", 
        "author": "Harper Lee"
    },
    {
        "id": 3, 
        "title": "1984", 
        "author": "George Orwell"
    },
]

@app.get("/books")
def get_books():
    return books

class Book(BaseModel):
    id: int
    title: str
    author: str

# Create a new book
@app.post("/books")
def add_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

# Retrieve a book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None

# Update a book by ID
@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            if book_update.title is not None:
                book["title"] = book_update.title
            if book_update.author is not None:
                book["author"] = book_update.author
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book by ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
