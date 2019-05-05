from bs4 import BeautifulSoup as BS
from bs4 import Comment
import sys
import requests

sayfa = sys.argv[1]

html = requests.get(sayfa)

html = html.content

kaynak_kodu=BS(html,'html.parser')

yorumlar = kaynak_kodu.find_all(string=lambda text:isinstance(text,Comment))

for i in yorumlar:
    print(i)
