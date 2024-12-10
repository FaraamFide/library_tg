import requests
from bs4 import BeautifulSoup


headers = {
   "Accept": "text/html",
   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
}



    
def write_list_of_books(author_name, data, path="tg_library/books", name_of_file="aaa_list_of_books.txt"):

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
        href = book.get('href').replace("/index.html", "")#.replace('/p.1', '')
        text = book.get_text()

        if "/author" not in href:
            href = f"/author/{author_name}" + href    

        #print(f'{href} --- {text}')
        data += f"{href} --- {text}\n"
    
    data = data.removesuffix("\n")
    return data


if __name__ == "__main__":

    with open('./tg_library/authors.txt', 'r', encoding='utf-8') as file:
        authors = file.read().split('\n')

    for author in authors:
        author = author.split(" -- ")[0]
        print(author)
        data = get_list_of_books(author_name=author)
        write_list_of_books(author_name=author, data=data)

    print("\n <--  END  -->")


