import re
from config import BOOKS_PATH, AUTHORS_PATH


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



def split_text_into_chunks(text, min_words=110):
    text = text.replace("\n", " \n")
    words = text.split(" ")
    
    chunks = []
    current_chunk = []
    word_count = 0

    sentence_end_pattern = re.compile(r'(\S+\s){2,}\S+[.!?]$')
    
    for word in words:
        current_chunk.append(word)
        word_count += 1
        

        if sentence_end_pattern.match(" ".join(current_chunk[-3:])) and word_count >= min_words:
            chunks.append(" ".join(current_chunk).strip())
            current_chunk = []
            word_count = 0


    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks







def escape_markdown(text):
    # Escapes all special characters for Markdown except supported formatting
    text = re.sub(r'(?<!\*)\*(?!\*)', r'\*', text)  # Escape single '*'
    text = re.sub(r'(?<!_)_(?!_)', r'\_', text)     # Escape single '_'
    text = re.sub(r'(?<!~)~(?!~)', r'\~', text)     # Escape single '~'
    text = re.sub(r'(?<!\_)__(?!\_)', r'\_\_', text)  # Escape unbalanced '__'
    text = re.sub(r'([`>\#+\-=|{}.!()])', r'\\\1', text)  # Escape other symbols
    return text



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


    

