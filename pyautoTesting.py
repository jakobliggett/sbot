import webbrowser
import requests, sys, webbrowser, bs4, os

#webbrowser.open('http://www.google.com')

res = requests.get('https://chrome.google.com/webstore/search/' + 'adblock')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)
linkElems = soup.select('.r a')
for i in range(len(linkElems)):
    webbrowser.open('http://chrome.google.com/webstore' + linkElems[i].get('href'))
