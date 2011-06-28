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

        # Encrypt a couple of login and password received RSA-key.
        self._crypt()

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

    def _crypt(self):
        """
        Encrypt a couple of login and password received RSA-key.
        see for detail: http://habrahabr.ru/blogs/firefox/83710/
        """

        NSTR, ESTR = self._key.split("#")
        credentials = '<credentials login="%s" password="%s"/>' % (self.username, self.password)
        DATA_ARR = [ord(x) for x in credentials]
        N, E, STEP_SIZE = int(NSTR, 16), int(ESTR, 16), len(NSTR) / 2 - 1

        prev_crypted = [0] * STEP_SIZE

        hex_out = ""
        for i in range(0, (len(DATA_ARR) - 1) / STEP_SIZE + 1):
            tmp = DATA_ARR[i * STEP_SIZE:(i + 1) * STEP_SIZE]
            tmp = [tmp[i] ^ prev_crypted[i] for i in range(0, len(tmp))]
            tmp.reverse()
            plain = 0
            for x in range(0, len(tmp)): plain += tmp[x] * pow(256, x, N)
            hex_result = "%x" % pow(plain, E, N)
            hex_result = "".join(['0'] * ( len(NSTR) - len(hex_result))) + hex_result

            for x in range(0, min(len(hex_result), len(prev_crypted) * 2), 2):
                prev_crypted[x / 2] = int(hex_result[x:x + 2], 16)

            hex_out += ("0" if len(tmp) < 16 else "") + ("%x" % len(tmp)) + "00" # current size
            ks = len(NSTR) / 2
            hex_out += ("0" if ks < 16 else "") + ("%x" % ks) + "00" # key size
            hex_out += hex_result

        self._rsa_key = hex_out.decode("hex").encode("base64").replace("\n", "")

if __name__ == '__main__':
    y = sync_yafotki("yafotkimytest123", "g2h9h4")
    
