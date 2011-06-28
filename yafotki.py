#-*- coding:utf-8 -*-
from Demos.win32cred_demo import username

__author__ = 'ponomarevsa@yandex.ru'

import urllib2

class sync_yafotki():
    """
    Downloading pictures from fotki.yandex.ru on local drive
    links:
        yandex.fotki api http://api.yandex.ru/fotki/
    """
    _request_key_url = 'http://auth.mobile.yandex.ru/yamrsa/key/'

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


if __name__ == '__main__':
    y = sync_yafotki("username")
    
