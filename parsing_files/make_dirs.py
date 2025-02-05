#make dirs for author 
if __name__ == "__main__":

    import os

    with open(r'C:\Users\user\Desktop\library_tg\authors.txt', 'r', encoding='utf-8') as file:
        authors = file.read()

    print(authors)

    for author in authors.split('\n'):
        a = author.split(' -- ')
        print(a[0])
        
        os.makedirs(f"tg_library/books/{a[0]}", exist_ok=True)
