import urllib.request, urllib.error
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

DOMAIN = 'www.bork.ru'
HOST = 'https://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:', 'https:']
links = set()  # множество всех ссылок
url = 'https://www.bork.ru/about/awards/'

def add_all_links_recursive(url, maxdepth=1):
    print(len(links))
    # извлекает все ссылки из указанного url
    # и рекурсивно обрабатывает их
    # глубина рекурсии не более maxdepth

    # список ссылок, от которых в конце мы рекурсивно запустимся
    links_to_handle_recursive = []

    # получаем html код страницы
    request = requests.get(url)
    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'html.parser')
    # рассматриваем все теги <a>
    for tag_a in soup.find_all('a'):
        # получаем ссылку, соответствующую тегу
        try:
            #print(tag_a)
            #print(tag_a['href'])
            link = tag_a['href']
        except KeyError:
            print(KeyError)
            print("Tag <a> haven't link - this is video or maps" + str(tag_a))
            # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            # проверяем, является ли ссылка относительной
            # например, /eShop --- это относительная ссылка
            # https://www.bork.ru/eShop --- это абсолютная ссылка
            if link.startswith('/') and not link.startswith('//'):
                # преобразуем относительную ссылку в абсолютную
                #print(link)
                link = HOST + link
                #print(link)
            # проверяем, что ссылка ведёт на нужный домен
            # и что мы ещё не обрабатывали такую ссылку
            if urlparse(link).netloc == DOMAIN and link not in links:
                print(link)

                url_test(link)
                links.add(link)
                links_to_handle_recursive.append(link)

    #print(links_to_handle_recursive)

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            print('NEXT PAGE: ' + link)
            add_all_links_recursive(link, maxdepth = maxdepth - 1)

def url_test(link):
    try:
        conn = urllib.request.urlopen(link)
    except urllib.error.HTTPError as e:
        # Обработка исключения при котором возвращаются ошибки URL(напр. 404, 501, ...)
        print('ERR: {}'.format(e.code))
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print('URL ERR: {}'.format(e.reason))
    except ValueError:
        print(ValueError)
        print('Uncorrect link')
    else:
        # 200
        print('OK')


def main():
    add_all_links_recursive(url, 1)
    for link in links:
        print(link)
    print('END WORK')


if __name__ == '__main__':
    main()

