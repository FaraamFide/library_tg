import re
from config import BOOKS_PATH, AUTHORS_PATH

# Функции для получения списка авторов и книг
def get_authors(path_to_authors=f"{AUTHORS_PATH}authors.txt"):
    with open(path_to_authors, "r", encoding="utf-8") as file:
        authors_array = file.read().replace("\xa0", " ").split("\n")
        
    authors = {}
    for author in authors_array:
        system_name, rus_name = author.split(" -- ")
        authors[system_name] = rus_name
    return authors

def get_list_of_books(author, path_to_folders=BOOKS_PATH):
    with open(f"{path_to_folders}/{author}/aaa_list_of_books.txt", "r", encoding="utf-8") as file:
        lines = file.read().split("\n")
    list_of_books = []
    for book in lines:
        if "/form" in book or "/theme" in book or "/extract" in book:
            continue
        list_of_books.append(book)
    return list_of_books




# Функция для разбивки текста на чанки
def split_text_into_chunks_old(text, min_chunk_size=340, max_chunk_size=400):
    text = text.replace("\n", " \n")
    words = text.split(" ")
    chunks = []
    chunk = []
    chunk_word_count = 0
    first_dot = False
    words_after_dot = 0

    for word in words:
        # Проверяем, если предложение заканчивается точкой и длинное
        if word.endswith((".", "?", "!")) and len(chunk) >= min_chunk_size:
            if not first_dot:
                first_dot = True
                continue

            if words_after_dot < 4:
                words_after_dot = 0

            if words_after_dot > 3:
                chunk.append(word)
                chunks.append(" ".join(chunk))
                chunk = []
                first_dot = False
                words_after_dot, chunk_word_count = 0, 0

            chunk_word_count += 1
            continue

        if first_dot and len(word) > 4 and "\n" not in word:
            words_after_dot += 1

        chunk.append(word)
        chunk_word_count += 1
        
    if chunk:
        chunks.append(" ".join(chunk))
    
    return chunks


def split_text_into_chunks(text, min_words=110):
    # Preprocessing text to handle newlines and spaces
    text = text.replace("\n", " \n")  # Ensuring newline remains detectable
    words = text.split(" ")  # Splitting text by space
    
    # Initialize variables for chunking
    chunks = []
    current_chunk = []
    word_count = 0

    # Define a pattern to check if a sentence ends with at least three words.
    sentence_end_pattern = re.compile(r'(\S+\s){2,}\S+[.!?]$')
    
    for word in words:
        current_chunk.append(word)
        word_count += 1
        
        # Check if the current word ends a sentence with 3+ words, and chunk has enough words
        if sentence_end_pattern.match(" ".join(current_chunk[-3:])) and word_count >= min_words:
            # Join the words to form a chunk and add it to chunks list
            chunks.append(" ".join(current_chunk).strip())
            # Reset for the next chunk
            current_chunk = []
            word_count = 0

    # Add any remaining text as the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks





# Экранирование спецсимволов для Markdown, кроме **...** и __...__ и ~~...~~
# def escape_markdown(text):
#     text = re.sub(r'([`>\#+\-=|{}.!()])', r'\\\1', text)
#     return text

def escape_markdown(text):
    # Escapes all special characters for Markdown except supported formatting
    text = re.sub(r'(?<!\*)\*(?!\*)', r'\*', text)  # Escape single '*'
    text = re.sub(r'(?<!_)_(?!_)', r'\_', text)     # Escape single '_'
    text = re.sub(r'(?<!~)~(?!~)', r'\~', text)     # Escape single '~'
    text = re.sub(r'(?<!\_)__(?!\_)', r'\_\_', text)  # Escape unbalanced '__'
    text = re.sub(r'([`>\#+\-=|{}.!()])', r'\\\1', text)  # Escape other symbols
    return text




# Загружаем книгу и делим её на главы
def split_to_chapters(book_path):
    with open(book_path, "r", encoding="utf-8") as file:
        return file.read().split("\nNEWCHAPTER\n")
    



#  "/author/bunin/text/3229/p.1" --> books/bunin/На пруде.txt
def href_to_path(link):
    def get_name_and_author(link):

        author = link.split("/")[2]

        with open(f"{BOOKS_PATH}/{author}/aaa_list_of_books.txt", "r", encoding="utf-8") as file:
            books = file.read().split("\n")
            for book in books:
                href, name = book.split(" --- ")
                if href == link:
                    return (author, name)
            
    author, name = get_name_and_author(link)
    path = f"{BOOKS_PATH}/{author}/{name}.txt"
    return path


    

