import pytest
from httpc.httpc import req
from httpc.httpc import parse_addr


class TestSite:
    def test_wikipedia(self):
        assert req('GET', 'ru.wikipedia.org', 'http', '/wiki/HTTP', 2024)\
               == "https://ru.wikipedia.org/wiki/HTTP"

    def test_vk_to_https(self):
        assert req('GET', 'vk.com', 'http', '/', 2024)\
               == "https://vk.com/"

    def test_vk_to_mvk(self):
        assert req('GET', 'vk.com', 'https', '/', 2024)\
               == "https://m.vk.com/"

    def test_parser(self):
        assert parse_addr('yandex.ru') == ('yandex.ru', 'http', '/')
        assert parse_addr('https://yandex.ru') == ('yandex.ru', 'https', '/')
        assert parse_addr('vk.com/feed') == ('vk.com', 'http', '/feed')
