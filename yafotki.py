#-*- coding:utf-8 -*-
import urllib
import urllib2
from BeautifulSoup import BeautifulStoneSoup

__author__ = 'ponomarevsa@yandex.ru'


class sync_yafotki():
    """
    Downloading pictures from fotki.yandex.ru on local drive
    links:
        yandex.fotki api http://api.yandex.ru/fotki/
    """
    _key = ""
    _request_id = ""
    _rsa_key = ""
    _token = ""
    _root_dir = r'c:\myfotki'

    _request_key_url = "http://auth.mobile.yandex.ru/yamrsa/key/"
    _request_token_url = "http://auth.mobile.yandex.ru/yamrsa/token/"
    _request_albums_url = "http://auth.mobile.yandex.ru/yamrsa/token/"

    def __init__(self, username="", password=""):
        """
        @param username
        @param password
        """

        # define username and password
        if username == "":
            self.username = raw_input("username: ")
        else:
            self.username = username

        if password == "":
            self.password = raw_input("password: ")
        else:
            self.password = password

        # Request the server to the public RSA-key.
        self._request_key();

    def _request_key(self):
        """
        Request the server to the public RSA-key and request_id.
        """
        req = urllib2.Request(self._request_key_url)
        xml = urllib2.urlopen(req).read()
        soup = BeautifulStoneSoup(xml)
        self._key = soup.key.string
        self._request_id = soup.request_id.string
        return True

if __name__ == '__main__':
    y = sync_yafotki("yafotkimytest123", "g2h9h4")
    
