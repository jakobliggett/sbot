import webbrowser
import requests, sys, webbrowser, bs4, os

#webbrowser.open('http://www.google.com')

res = requests.get('http://google.com/search?q=' + 'eddie')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "html5lib")
linkElems = soup.select('.r a')
for i in range(len(linkElems)):
    webbrowser.open('http://google.com' + linkElems[i].get('href'))