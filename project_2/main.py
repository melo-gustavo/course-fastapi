from typing import Optional

from fastapi import FastAPI, HTTPException

import uvicorn
from pydantic import BaseModel, Field

from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookSchema(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5)
    author: str = Field(min_length=5)
    description: str = Field(min_length=10, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Lord of Rings",
                "author": "Gustavo Melo",
                "description": "This is a very good book.",
                "rating": 5,
                "published_date": 2012
            }
        }


books = [
    Book(1, "Book 1", "Author 1", "Description 1", 5, 2014),
    Book(2, "Book 2", "Author 2", "Description 2", 5, 2013),
    Book(3, "Book 3", "Author 3", "Description 3", 4, 2014),
    Book(4, "Book 4", "Author 4", "Description 4", 3, 2012),
    Book(5, "Book 5", "Author 5", "Description 5", 3, 2023)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books


@app.get("/books/rating", status_code=status.HTTP_200_OK)
async def get_rating_books(rating: int):
    rating = False
    ratings_equals = []
    for book in books:
        if book.rating == rating:
            ratings_equals.append(book)
            rating = True
            return ratings_equals

    if not rating:
        raise HTTPException(status_code=404, detail="Item not found!")


@app.get("/books/published_date", status_code=status.HTTP_200_OK)
async def get_published_date_book(published_date: int):
    published = False
    published_books = []
    for book in books:
        if book.published_date == published_date:
            published_books.append(book)
            published = True
            return published_books

    if not published:
        raise HTTPException(status_code=404, detail="Item not found!")


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_single_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found!")


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(data: BookSchema):
    book = Book(**data.dict())
    books.append(increment_id(book))

    return books


def increment_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book


@app.put("/update-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int, data: BookSchema):
    updated_book = False
    for i in range(len(books)):
        if books[i].id == book_id:
            books[i] = data
            updated_book = True
            return books
    if not updated_book:
        raise HTTPException(status_code=404, detail="Item not found!")


@app.delete("/book", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    deleted_book = False
    for book in books:
        if book.id == book_id:
            books.remove(book)
            deleted_book = True

    if not deleted_book:
        raise HTTPException(status_code=404, detail="Item not found!")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)
