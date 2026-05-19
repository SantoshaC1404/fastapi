from fastapi import FastAPI, Depends
import model
from database import get_db, Base, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Create the FastAPI app
app = FastAPI()

class BookStore(BaseModel):
    id: int
    title: str
    author: str

@app.post("/books")
def create_books(book: BookStore, db: Session = Depends(get_db)):
    new_book = model.Books(id=book.id, title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books")
def getall_books(db: Session = Depends(get_db)):
    books = db.query(model.Books).all()
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(model.Books).filter(model.Books.id == book_id).first()
    if book is None:
        return {"message": "Book not found"}
    return book