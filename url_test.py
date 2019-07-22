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

    links_to_handle_recursive = []

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    for tag_a in soup.find_all('a'):
        try:
            #print(tag_a)
            #print(tag_a['href'])
            link = tag_a['href']
        except KeyError:
            print("\n")
            print(KeyError)
            print("\n")
            print("Tag <a> haven't link - this is video or maps\n" + "\n" + str(tag_a))
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            if link.startswith('/') and not link.startswith('//'):
                #print(link)
                link = HOST + link
                #print(link)
            if urlparse(link).netloc == DOMAIN and link not in links:
                print(link)

                url_test(link)
                links.add(link)
                links_to_handle_recursive.append(link)

    #print(links_to_handle_recursive)

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            print("\n")
            print('NEXT PAGE: ' + link)
            add_all_links_recursive(link, maxdepth = maxdepth - 1)

def url_test(link):
    try:
        conn = urllib.request.urlopen(link)
    except urllib.error.HTTPError as e:
        # Обработка исключения при котором возвращаются ошибки URL(напр. 404, 501, ...)
        print('ERR: {}'.format(e.code))
    except urllib.error.URLError as e:
        # Другие ошибки(напр. отказано в подключении)
        print('URL ERR: {}'.format(e.reason))
    except ValueError:
        print("\n")
        print(ValueError)
        print("\n")
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

