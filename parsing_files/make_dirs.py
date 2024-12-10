#make dirs for author 
if __name__ == "__main__":

    import os

    with open('./tg_library/authors.txt', 'r', encoding='utf-8') as file:
        authors = file.read()

    print(authors)

    for author in authors.split('\n'):
        a = author.split(' -- ')
        #a[1] = a[1].replace(u'\xa0', u' ')
        #a[1] = a[1].replace(u'.', u'')
        print(a[0])
        
        os.makedirs(f"tg_library/books/{a[0]}", exist_ok=True)