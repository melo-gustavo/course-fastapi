from fastapi import FastAPI

import uvicorn

app = FastAPI()


books = [
    {"title": "Title One", "author": "Author One"},
    {"title": "Title Two", "author": "Author Two"},
    {"title": "Title Three", "author": "Author Three"},
    {"title": "Title Four", "author": "Author Four"},
    {"title": "Title Five", "author": "Author Five"}
]


@app.get("/")
async def all_books():
    return books


@app.get("/books/bytitle/{book_title}")
async def single_book(book_title: str):
    for book in books:
        if book["title"] == book_title:

            return book


@app.get("/books/byauthor/{author}")
async def get_books_by_author(author: str):
    books_by_author = []
    for book in books:
        if book["author"] == author:
            books_by_author.append(book)

    return books_by_author


@app.post("/book")
async def create_book(title: str, author: str):
    if title and author is not None:
        book = {
            "title": title,
            "author": author
        }
        books.append(book)

    return book


@app.put("/books/{book_title}")
async def update_book(book_title: str, title: str, author: str):
    update_book = None
    for book in books:
        if book["title"] == book_title:
            book["title"] = title
            book["author"] = author
            update_book = book

    return update_book


@app.delete("/book")
async def delete_book(title: str):
    count = 0
    for book in books:
        if book["title"] == title:
            books.pop(count)
        count += 1

    return books


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
