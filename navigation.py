from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import MAX_BOOKS_PER_PAGE
from utils import get_list_of_books

def works_menu(author_key, page=0):
    print("works_menu")
    markup = InlineKeyboardMarkup()
    books = get_list_of_books(author_key)
    start = page * MAX_BOOKS_PER_PAGE
    end = start + MAX_BOOKS_PER_PAGE
    books_on_page = books[start:end]

    for book in books_on_page:
        link, title = book.split(" --- ")
        markup.add(InlineKeyboardButton(title, callback_data=f"work_{link}"))

    if page > 0:
        markup.row(InlineKeyboardButton("⬅️ Предыдущая страница", callback_data=f"page_{author_key}_{page-1}"))
    if end < len(books):
        markup.row(InlineKeyboardButton("➡️ Следующая страница", callback_data=f"page_{author_key}_{page+1}"))

    return markup

def books_menu(found_books, page=0, query=""):
    print("books_menu")
    markup = InlineKeyboardMarkup()
    start = page * MAX_BOOKS_PER_PAGE
    end = start + MAX_BOOKS_PER_PAGE

    books_on_page = found_books[start:end]

    for link, title, author_name in books_on_page:
        if query == "MimeAuthors":
            markup.add(InlineKeyboardButton(f"{title}", callback_data=f"author_{author_name}"))
        else:
            markup.add(InlineKeyboardButton(f"{title} ({author_name})", callback_data=f"work_{link}"))

    if page > 0:
        markup.row(InlineKeyboardButton("⬅️ Предыдущая страница", callback_data=f"bookpage_{page-1}_{query}"))
    if end < len(found_books):
        markup.row(InlineKeyboardButton("➡️ Следующая страница", callback_data=f"bookpage_{page+1}_{query}"))

    return markup






 
