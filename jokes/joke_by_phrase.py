from abc import ABC
from random import choice
import requests
from html.parser import HTMLParser


class Parser(HTMLParser, ABC):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.data = []
        self.joke = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs[0][1] == 'text':
            self.flag = True
        if tag == 'br':
            self.joke += '\n'

    def handle_data(self, data):
        if self.flag:
            self.joke += data

    def handle_endtag(self, tag):
        if tag == 'div' and self.flag:
            self.flag = False
            self.data.append(self.joke)
            self.joke = ''


def get_joke_by_phrase(phrase) -> list:
    resp = requests.post('https://nekdo.ru/search', data={'query': phrase}).content.decode()
    parser = Parser()
    parser.feed(resp)
    return choice(parser.data)

