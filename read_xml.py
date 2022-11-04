from bs4 import BeautifulSoup
import os

file = open ('xml/61-2019-01.xml','r').read()
soup = BeautifulSoup(file, 'xml')

data = {}
# soup = BeautifulSoup(filename, 'lxml')
abstract = ""

for tag in soup.find_all('title'):
    if tag.text.strip() == 'Abstract':
        print("tag contain   **  " + str(tag.text));
        for p in tag.parent.find_all('p'):
            abstract += p.text
            print("p:   **  "+str(p));
            # data['Abstract'] = abstract.strip()
        
# print(data)