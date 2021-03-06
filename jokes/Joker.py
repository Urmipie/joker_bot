from . import joke_by_phrase
from . import random_joke


class Joker:
    def __init__(self):
        self._get_random_jokes()

    def _random_joke(self):
        if not self.random_jokes:
            self._get_random_jokes()
        joke = self.random_jokes.pop()
        return f'{joke}\n\nАнекдот с anekdot.ru'

    def _get_random_jokes(self):
        self.random_jokes = random_joke.random_joke()

    def get_joke(self, phrase=''):
        if phrase:
            return f'{joke_by_phrase.get_joke_by_phrase(phrase)}\n\nАнекдот с nekdo.ru'
        else:
            return self._random_joke()
