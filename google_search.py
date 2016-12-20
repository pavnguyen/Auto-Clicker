import bs4
import requests

print('Googling...')
res = requests.get('https://encrypted.google.com/search?q=ABC song')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
linkElems = soup.select('.r a')
for i in range(3):
    url_ytb = 'https://www.google.com' + linkElems[i].get('href')
    print(url_ytb)
    print(linkElems[i].getText())
