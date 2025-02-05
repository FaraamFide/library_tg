import requests
from bs4 import BeautifulSoup

def correctName(name):
    zapret = "!?<>@$%*^;:~.,`\'\"\\/«»"
    res = ""
    for i in name:
        if i not in zapret:
            res += i
    return res

headers = {
   "Accept": "text/html",
   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
}



    
def write_list_of_books(author_name, data, path=r'C:\Users\user\Desktop\library_tg\books', name_of_file="aaa_list_of_books.txt"):

     with open(f"{path}/{author_name}/{name_of_file}", "w", encoding="utf-8") as file:
        file.write(data) 


def get_list_of_books(author_name):
    req = requests.get(f"https://ilibrary.ru/author/{author_name}/l.all/index.html", headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    books = soup.find_all('p')

    data = ""
    for book in books:
        book = book.find('a')
        href = book.get('href').replace("/index.html", "")
        text = book.get_text()

        if "/author" not in href:
            href = f"/author/{author_name}" + href
        text = correctName(text)
        #print(text, "AFDjAIFALWKHGFwUHfgaiLWU")
        data += f"{href} --- {text}\n"
    
    data = data.removesuffix("\n")
    return data


if __name__ == "__main__":

    with open(r'C:\Users\user\Desktop\library_tg\authors.txt', 'r', encoding='utf-8') as file:
        authors = file.read().split('\n')

    for author in authors:
        author = author.split(" -- ")[0]
        print(author)
        data = get_list_of_books(author_name=author)
        write_list_of_books(author_name=author, data=data)

    print("\n <--  END  -->")


