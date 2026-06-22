"""
Нужно парсить страницу со свежими статьями (https://habr.com/ru/all/) и выбирать те статьи,
в которых встречается хотя бы одно из ключевых слов.
Эти слова определяем в начале скрипта.
Поиск вести по всей доступной preview-информации, т. е. по информации, доступной с текущей страницы.
Выведите в консоль список подходящих статей в формате: <дата> – <заголовок> – <ссылка>.
"""


import requests
from bs4 import BeautifulSoup

# ---------- НАСТРОЙКИ ----------
KEYWORDS = ['Северная Звезда', 'Туториал', 'DevOps ', 'web', 'python']
BASE_URL = 'https://habr.com'
URL = BASE_URL + '/ru/articles/' #https://habr.com/ru/all/ Status Code 302 Found --> location https://habr.com/ru/articles/

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# ---------- ЗАГРУЗКА СТРАНИЦЫ ----------
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, features='lxml')

# ---------- ПАРСИНГ СТАТЕЙ ----------
articles = soup.find_all('article', class_='tm-articles-list__item')

found_posts = []

for article in articles:
    # 1. Дата
    time_tag = article.find('time')
    if time_tag and time_tag.get('datetime'):
        date = time_tag['datetime']
    else:
        date = 'Дата не указана'

    # 2. Заголовок и ссылка
    title_tag = article.find('a', class_='tm-title__link')
    if not title_tag:
        continue
    title = title_tag.text.strip()
    link = BASE_URL + title_tag['href']

    # 3. Собираем всю доступную информацию из карточки для поиска
    #    - заголовок
    full_text = title + ' '

    #    - текст превью (все блоки article-formatted-body)
    preview_divs = article.find_all('div', class_=lambda c: c and 'article-formatted-body' in c)
    for div in preview_divs:
        full_text += div.text.strip() + ' '

    #    - названия хабов (ссылки с классом tm-publication-hub__link)
    hub_links = article.find_all('a', class_='tm-publication-hub__link')
    for hub in hub_links:
        full_text += hub.text.strip() + ' '

    #    - лейблы (метки, например "Кейс", "Туториал" и т.п.)
    #      Они находятся внутри div с классом tm-article-labels__container, внутри span с классом publication-label
    label_spans = article.find_all('span', class_='publication-label')
    for label in label_spans:
        full_text += label.text.strip() + ' '

    # 4. Проверяем, есть ли в собранном тексте хотя бы одно ключевое слово
    full_text_lower = full_text.lower()
    if any(keyword.lower() in full_text_lower for keyword in KEYWORDS):
        found_posts.append((date, title, link))

# ---------- ВЫВОД РЕЗУЛЬТАТОВ ----------
if found_posts:
    print('Найдены статьи:')
    for date, title, link in found_posts:
        print(f'{date} – {title} – {link}')
else:
    print('Статей с заданными ключевыми словами не найдено.')