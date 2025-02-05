
import os, requests
from bs4 import BeautifulSoup
import html


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Accept': 'text/html'
}




with open(r'C:\Users\user\Desktop\library_tg\authors.txt', 'r', encoding='utf-8') as file:
    authors = file.read().split('\n')


def write_books(book_url, book_name, author_name=None):
    inside_fns_div = False  # Выноска, тк дублируется внутри изза тега z
    chapter = 0
    cur_chapter = book_url.split(".")[-1]
    book_url = book_url.removeprefix(f"/author/{author_name}")

    req = requests.get(f"https://ilibrary.ru{book_url}/index.html", headers)
    req.encoding = "windows-1251" #utf-8"
    src = req.text.replace("&#151;","—")

    soup = BeautifulSoup(src, 'lxml')
    title = soup.find("h1")
    data = ""
    if title != None:
        data += title.text
        data += '\n\n'
    rf'C:\Users\user\Desktop\library_tg\books\{author}\{book_name}.txt'
    # with open(f"/books/{author}/{book_name}.txt", 'w', encoding='utf-8') as file:
    with open(rf'C:\Users\user\Desktop\library_tg\books\{author}\{book_name}.txt', 'w', encoding='utf-8') as file:
        file.write(data)

    #For 1 chapter books
    if (soup.find("div", class_="navlnktxt") == None) or (cur_chapter != "1"):
        data = ""
        content_div = soup.find("div", {"id": "text"})

        for element in content_div.descendants:
            if element.name in ["h2", "h3", "h4", "h5", "h6"]:
                    data += f"\n\t\t*{element.get_text()}*\n"

            elif element.name == "div" and "fns" in (element.get("class") or []):
                    data += f"\t__{element.get_text()}__\n"
                    inside_fns_div = True
                    continue

            elif element.name == "z" and not inside_fns_div:
                data += f"\t{element.get_text()}\n"


            if inside_fns_div and element.name == "div" and "fns" not in (element.get("class") or []):
                inside_fns_div = False



        with open(rf'C:\Users\user\Desktop\library_tg\books\{author}\{book_name}.txt', 'a', encoding='utf-8') as file:
            file.write(data)
        return

    exit_flag = True
    while exit_flag:
        
        
        
        
        while soup.find("div", class_="ang ra1") != None:
            chapter += 1
            if chapter != 1:
                with open(rf'C:\Users\user\Desktop\library_tg\books\{author}\{book_name}.txt', 'a', encoding='utf-8') as file:
                    file.write("\nNEWCHAPTER\n")
                    
            book_url = book_url.removesuffix("1")
            req = requests.get(f"https://ilibrary.ru{book_url}{chapter}/index.html", headers)

            req.encoding = "windows-1251"
            src = req.text.replace("&#151;","—")
            soup = BeautifulSoup(src, 'lxml')

            data = ""
        
    
            content_div = soup.find("div", {"id": "text"})
                
            for element in content_div.descendants:
                if element.name in ["h2", "h3", "h4", "h5", "h6"]:
                    data += f"\n\t\t*{element.get_text()}*\n"

                elif element.name == "div" and "fns" in (element.get("class") or []):
                    data += f"\t__{element.get_text()}__\n"
                    inside_fns_div = True
                    continue

                elif element.name == "z" and not inside_fns_div:
                    data += f"\t{element.get_text()}\n"


                if inside_fns_div and element.name == "div" and "fns" not in (element.get("class") or []):
                    inside_fns_div = False

               

            with open(rf'C:\Users\user\Desktop\library_tg\books\{author}\{book_name}.txt', 'a', encoding='utf-8') as file:
                file.write(data)
                
            break
                
        else:
            exit_flag = False
            

    
    
with open(r'C:\Users\user\Desktop\library_tg\authors.txt', 'r', encoding='utf-8') as file:
    authors = file.read().split('\n')


import time

go = False
for author in authors:
    author = author.split(" -- ")[0]
    count = 0
    new_count = 0
    with open(rf"C:\Users\user\Desktop\library_tg\books\{author}\aaa_list_of_books.txt", "r", encoding="utf-8") as file:
        books = file.readlines()
        for book in books:
            count += 1
            book = book.split(" --- ")
            href, name = book[0], book[1].strip("\n")   #     /author/unknown/text/1375/p.1 Слово о полку Игореве

            if "theme" in href or "form" in href:
                continue

            if os.path.exists(rf"C:\Users\user\Desktop\library_tg\books\{author}\{name}.txt"):
                print("skip")
                continue


            write_books(href, name, author)
            print(name)
            new_count += 1
    print(f"{author} -- done. Written new {new_count} books, total - {count}")

print("END -----------------------------------------------------------------------------------")
