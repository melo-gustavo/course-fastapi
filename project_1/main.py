from fastapi import FastAPI

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


@app.get("/books/{book_title}")
async def single_book(book_title: str):
    for book in books:
        if book["title"] == book_title:

            return book


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
