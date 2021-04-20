import requests


def random_joke():
    a = requests.get('https://www.anekdot.ru/rss/randomu.html').content.decode()
    a = a.split('[\\"')[1].split('\\"]')[0].replace('<br>', '\n').replace('\\\\\\"', '"').split('\\",\\"')
    return a


if __name__ == '__main__':
    print(*random_joke(), sep='\n-------------\n')