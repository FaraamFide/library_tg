import re
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import (
    get_authors, get_list_of_books, split_text_into_chunks,
    split_to_chapters, escape_markdown, href_to_path
)
from config import MAX_BOOKS_PER_PAGE, MAX_FOUND_BOOKS, MAX_AUTHORS_PER_PAGE
from navigation import works_menu, books_menu


authors = get_authors()
authors_list = [[key, name] for key, name in authors.items()]

last_mes = None
chapters = []


def register_handlers(dp):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(choose_author, commands=['author'])
    dp.register_message_handler(choose_book, commands=['book'])
    dp.register_message_handler(list_authors, commands=['authors'])

    dp.register_callback_query_handler(process_callback, lambda c: c.data in ["prev_part", "next_part", "select_chapter", "next_chapter", "prev_chapter"])
    dp.register_callback_query_handler(process_chapter_selection, lambda c: c.data.startswith("chapter_"))
    dp.register_callback_query_handler(show_author_works, lambda c: c.data.startswith("author_"))
    dp.register_callback_query_handler(change_page, lambda c: c.data.startswith("page_"))
    dp.register_callback_query_handler(change_book_page, lambda c: c.data.startswith("bookpage_"))
    dp.register_callback_query_handler(show_work, lambda c: c.data.startswith("work_"))


from data_store import load_data
mes_to_execute_and_position = load_data()

async def list_authors(message: types.Message, page=0, query=""):
    authors1 = [("", i[1], i[0]) for i in authors_list]
    run_in_all()
    user_id = message.from_user.id
    message_to_delete_user = message.message_id
    if  mes_to_execute_and_position[str(user_id)]["authors_user"] != []:
        await delete_bot_message("authors_user", user_id)
        await delete_bot_message("authors", user_id)

    message_to_delete = await message.answer(escape_markdown("Авторы:"), reply_markup=books_menu(authors1, query="MimeAuthors"))
    mes_to_execute_and_position[str(user_id)]["authors"].append(message_to_delete.message_id)
    mes_to_execute_and_position[str(user_id)]["authors_user"].append(message_to_delete_user)



import inspect
def run_in_all():  # Func for debug
    frame = inspect.currentframe()
    frame_info = inspect.getframeinfo(frame.f_back)
    function_name = frame_info.function
    print(f"Название функции: {function_name}")


async def delete_bot_message(tag, u_id, max_count=1):
    run_in_all()
    from bot import bot
    
    if len(mes_to_execute_and_position[str(u_id)][tag]) >= max_count:
        try:
            await bot.delete_message(chat_id=u_id, message_id=mes_to_execute_and_position[str(u_id)][tag].pop(0))        
        except:
            print("ERROR WHILE DELETING MESSAGE")

async def send_welcome(message: types.Message):
    from bot import bot
    run_in_all()
    user_id = message.from_user.id
    
    if str(user_id) not in mes_to_execute_and_position.keys():
        mes_to_execute_and_position[str(user_id)] = {"work":[], "author_works":[], "author": [],"authors":[], "authors_user":[],
          "found_works":[], "found_works_user":[], "work_name": [], "start":[], "start_user": [],  "user_position": None}

    welcome_text = (
        "Привет! Я помогу вам найти произведения по авторам и названиям. Доступные команды:\n"
        "/author <имя автора> — найти автора и посмотреть его произведения\n"
        "/book <название книги> — найти книгу по названию и показать подходящие варианты\n"
        "/start — показать это сообщение\n"
        "/authors — вывести доступных авторов"
    )
    message_to_delete = await message.answer(escape_markdown(welcome_text))
    

    if mes_to_execute_and_position[str(user_id)]["start"] != []:
      
        await delete_bot_message("start", user_id)
        
    if  mes_to_execute_and_position[str(user_id)]["start_user"] != []:
        await delete_bot_message("start_user", user_id)
        

    mes_to_execute_and_position[str(user_id)]["start"].append(message_to_delete.message_id)
    mes_to_execute_and_position[str(user_id)]["start_user"].append(message.message_id)

async def choose_author(message: types.Message):
    run_in_all()
    query = message.get_args().strip()

    user_id = message.from_user.id

    if mes_to_execute_and_position[str(user_id)]["author"] != []:
        await delete_bot_message("author", user_id, max_count=2)


    if not query:
        message_to_delete = await message.answer(escape_markdown("Введите имя автора после команды, например: /author Пушкин"))
        mes_to_execute_and_position[str(user_id)]["author"].append(message_to_delete.message_id)
        return

    found_authors = {key: name for key, name in authors.items() if re.search(query, name, re.IGNORECASE)}

    if found_authors:
        if len(found_authors) == 1:
            author_key = list(found_authors.keys())[0]
            message_to_delete = await message.answer(escape_markdown(f"Произведения {found_authors[author_key]}:"), reply_markup=works_menu(author_key))
        else:
            markup = InlineKeyboardMarkup()
            for author_key, author_name in found_authors.items():
                markup.add(InlineKeyboardButton(author_name, callback_data=f"author_{author_key}"))
            message_to_delete = await message.answer(escape_markdown("Найдено несколько авторов, выберите одного из них:"), reply_markup=markup)
    else:
        message_to_delete = await message.answer(escape_markdown("Автор не найден. Попробуйте ввести другое имя или часть имени."))

    mes_to_execute_and_position[str(user_id)]["author"].append(message_to_delete.message_id)

async def show_author_works(callback_query: types.CallbackQuery):
    run_in_all()
    user_id = callback_query.from_user.id
    if  mes_to_execute_and_position[str(user_id)]["author"] != []: 
        await delete_bot_message("author", user_id, max_count=2)
        
    author_key = callback_query.data.split("_")[1]
    message_to_delete = await callback_query.message.answer(escape_markdown(f"Произведения {authors[author_key]}:"), reply_markup=works_menu(author_key))
    await callback_query.answer()

    mes_to_execute_and_position[str(user_id)]["author"].append(message_to_delete.message_id)

async def change_page(callback_query: types.CallbackQuery):
    run_in_all()
    _, author_key, page = callback_query.data.split("_")
    page = int(page)
    await callback_query.message.edit_text(escape_markdown(f"Произведения {authors[author_key]}:"), reply_markup=works_menu(author_key, page))
    await callback_query.answer()

async def choose_book(message: types.Message):
    run_in_all()

    user_id = message.from_user.id
    message_to_delete_user = message.message_id

    if  mes_to_execute_and_position[str(user_id)]["found_works"] != []:
        await delete_bot_message("found_works", user_id)
    
    if  mes_to_execute_and_position[str(user_id)]["found_works_user"] != []:
        await delete_bot_message("found_works_user", user_id)

    query = message.get_args().strip()
    if not query:
        message_to_delete = await message.answer(escape_markdown("Введите название книги после команды, например: /book Гроза"))
        mes_to_execute_and_position[str(user_id)]["found_works"].append(message_to_delete.message_id)
        mes_to_execute_and_position[str(user_id)]["found_works_user"].append(message_to_delete_user)
        return

    found_books = []
    for author_key, author_name in authors.items():
        books = get_list_of_books(author_key)
        for book in books:
            link, title = book.split(" --- ")
            if re.search(query, title, re.IGNORECASE):
                found_books.append((link, title, author_name))

    if found_books:
        message_to_delete = await message.answer(escape_markdown("Найденные произведения:"), reply_markup=books_menu(found_books, query=query))
    else:
        message_to_delete = await message.answer(escape_markdown("Произведение не найдено. Попробуйте ввести другое название или его часть."))


    mes_to_execute_and_position[str(user_id)]["found_works"].append(message_to_delete.message_id)
    mes_to_execute_and_position[str(user_id)]["found_works_user"].append(message_to_delete_user)

async def change_book_page(callback_query: types.CallbackQuery):
    run_in_all()
    data = callback_query.data.split("_")
    page = int(data[1])
    query = data[2]

    if query == "MimeAuthors":
        authors1 = [("", i[1], i[0]) for i in authors_list]
        await callback_query.message.edit_text(escape_markdown("Авторы:"), reply_markup=books_menu(authors1, page, query))
        await callback_query.answer()
        
    else:
        found_books = []
        for author_key, author_name in authors.items():
            books = get_list_of_books(author_key)
            for book in books:
                link, title = book.split(" --- ")
                if re.search(query, title, re.IGNORECASE):
                    found_books.append((link, title, author_name))

        await callback_query.message.edit_text(escape_markdown("Найденные произведения:"), reply_markup=books_menu(found_books, page, query))
        await callback_query.answer()

async def show_work(callback_query: types.CallbackQuery):
    from bot import bot
    run_in_all()
    work_link = callback_query.data[5:]
    global chapters
    chapters = split_to_chapters(href_to_path(work_link))

    user_id = callback_query.from_user.id
    mes_to_execute_and_position[str(user_id)]["user_position"] = {'chapter': 0, 'part': 0, 'chapters': chapters}

    await send_chapter_part(user_id, chapters)
    await callback_query.answer()

async def send_chapter_part(user_id, chapters=None):
    from bot import bot
    run_in_all()

    
    if not chapters:
        chapters = mes_to_execute_and_position[str(user_id)]["user_position"].get("chapters")
        
    chapter_index = mes_to_execute_and_position[str(user_id)]["user_position"]["chapter"]
    part_index = mes_to_execute_and_position[str(user_id)]["user_position"]["part"]
    chapter_parts = split_text_into_chunks(chapters[chapter_index])
    
    if part_index >= len(chapter_parts):
        part_index = len(chapter_parts) - 1

    part_text = escape_markdown(chapter_parts[part_index])
    keyboard = InlineKeyboardMarkup(row_width=3)

    if chapter_index > 0 and part_index == 0:
        keyboard.insert(InlineKeyboardButton("Назад", callback_data="prev_chapter"))
    if part_index > 0:
        keyboard.insert(InlineKeyboardButton("<<", callback_data="prev_part"))
    if len(chapters) > 1:
        chapter_part_text = escape_markdown(f"Глава {chapter_index + 1}\n{part_index + 1}/{len(chapter_parts)}")
        keyboard.insert(InlineKeyboardButton(chapter_part_text, callback_data="select_chapter"))
    if part_index < len(chapter_parts) - 1:
        keyboard.insert(InlineKeyboardButton(">>", callback_data="next_part"))
    elif chapter_index < len(chapters) - 1:
        keyboard.insert(InlineKeyboardButton("Далее", callback_data="next_chapter"))

    
    if mes_to_execute_and_position[str(user_id)]["work"] != []:
        try:
            await bot.delete_message(chat_id=user_id, message_id=mes_to_execute_and_position[str(user_id)]["work"].pop(0))
        except:
            pass

    message_to_delete = await bot.send_message(user_id, part_text, reply_markup=keyboard)
    mes_to_execute_and_position[str(user_id)]["work"].append(message_to_delete.message_id) 


async def process_callback(callback_query: types.CallbackQuery):
    run_in_all()
    user_id = callback_query.from_user.id
    action = callback_query.data

    if action == "select_chapter":
        await show_chapter_selection(user_id, callback_query.message.message_id)
        return

    if action == "next_part":
        mes_to_execute_and_position[str(user_id)]["user_position"]["part"] += 1
        
    elif action == "prev_part":
        mes_to_execute_and_position[str(user_id)]["user_position"]["part"] -= 1
        
    elif action == "next_chapter":
        mes_to_execute_and_position[str(user_id)]["user_position"]["chapter"] += 1
        mes_to_execute_and_position[str(user_id)]["user_position"]["part"] = 0
        
    elif action == "prev_chapter":
        mes_to_execute_and_position[str(user_id)]["user_position"]["chapter"] -= 1
        mes_to_execute_and_position[str(user_id)]["user_position"]["part"] = len(split_text_into_chunks(mes_to_execute_and_position[str(user_id)]["user_position"]["chapters"][mes_to_execute_and_position[str(user_id)]["user_position"]["chapter"]])) -1

    await send_chapter_part(user_id, chapters)

async def show_chapter_selection(user_id, message_id):
    run_in_all()
    from bot import bot
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in range(len(mes_to_execute_and_position[str(user_id)]["user_position"]["chapters"])):
        chapter_button = InlineKeyboardButton(escape_markdown(f"ГЛАВА {i + 1}"), callback_data=f"chapter_{i}")
        keyboard.add(chapter_button)

    await bot.edit_message_text(escape_markdown("Выберите главу:"), chat_id=user_id, message_id=message_id, reply_markup=keyboard)

async def process_chapter_selection(callback_query: types.CallbackQuery):
    run_in_all()
    chapter_index = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id
    mes_to_execute_and_position[str(user_id)]["user_position"]["chapter"] = chapter_index
    mes_to_execute_and_position[str(user_id)]["user_position"]["part"] = 0
    await send_chapter_part(user_id, chapters)
    await callback_query.answer()
