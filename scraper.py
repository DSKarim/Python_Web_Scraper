import requests
from bs4 import BeautifulSoup
import string
import os
import shutil


saved_articles = []
type_classes = {'new': 'c-article-body', 'research highlight': 'article-item__body'}

num_pages = int(input())
type_article = input().lower()

i = 1
while i <= num_pages:
    if os.path.exists('Page_' + str(i)):
        shutil.rmtree('Page_' + str(i))
    os.mkdir('Page_' + str(i))
    os.chdir('Page_' + str(i))
    r = requests.get('https://www.nature.com/nature/articles?year=2020', params={'page' : f'{i}'})

    soup = BeautifulSoup(r.content, 'html.parser')

    articles = soup.find_all('article')
    for art in articles:
        if art.find('span', {'data-test': 'article.type'}).text.strip('\n').lower() == type_article:
            title = art.find("h3", {"class": "c-card__title"}).text.strip('\n')
            title = title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')

            link = art.find('a', {'data-track-action': 'view article'})
            content_page = requests.get('https://www.nature.com' + link['href'], headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup_bis = BeautifulSoup(content_page.content, 'html.parser')
            content_body = soup_bis.find('div', {'class': type_classes.get(type_article, 'c-article-body')}).text.strip()
            with open(title + '.txt', 'wb') as f:
                f.write(content_body.encode('utf-8'))
            saved_articles.append(title + '.txt')
    os.chdir('..')
    i += 1

print('Saved articles:\n', saved_articles)
