import requests
from bs4 import BeautifulSoup

st_accept = "text/html" 
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}


req = requests.get("https://ilibrary.ru/author.html", headers)
src = req.text


soup = BeautifulSoup(src, 'lxml')
authors = soup.find('div', class_='l')#.find_all('li')



def parse_and_save_links(soup, output_file):
    links = soup.find_all('a')
    print(links)
    with open(output_file, 'w', encoding='utf-8') as file:
        for link in links:
            href = link.get('href').replace("/index.html", "").replace("/author/", "")
            print(href)
            text = link.get_text()
            file.write(f"{href} -- {text}\n")



if __name__ == "__main__":
    output_file_path = 'authors.txt'
    parse_and_save_links(authors, output_file_path)
    print(f"Ссылки и имена авторов сохранены в {output_file_path}")
