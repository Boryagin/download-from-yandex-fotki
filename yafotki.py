#-*- coding:utf-8 -*-
import os
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
    _request_albums_url = 'http://api-fotki.yandex.ru/api/users/%s/albums/'

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

        # Exchange encrypted login and password for the authorization token.
        self._request_token()

        # Download albums
        self._download()

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
        @author http://lomik.habrahabr.ru/
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

    def _request_token(self):
        """
        Request the server to the public RSA-key and request_id.
        """
        values = {
            "request_id": self._request_id,
            "credentials": self._rsa_key
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(self._request_token_url, data)
        response = urllib2.urlopen(req)
        xml = response.read()
        soup = BeautifulStoneSoup(xml)
        self._token = soup.token.string
        if self._token != "":
            return True
        else:
            print xml
            exit()

    def _download(self):
        """
        download fotki
        """
        if not os.path.exists(self._root_dir): os.makedirs(self._root_dir)

        url = self._request_albums_url % self.username
        req = urllib2.Request(url)
        req.add_header('Authorization', 'FimpToken realm="fotki.yandex.ru", token="' + self._token + '"')
        xml = urllib2.urlopen(req).read()
        soup = BeautifulStoneSoup(xml)

        # href => key associate array
        all_ids_by_href = {}
        for entry in soup('entry'):
            all_ids_by_href[entry.findNext('link', rel="self")['href']] = entry.findNext('id').string

        # find all parents
        albums = []
        for link in soup('link'):
            if link["rel"] != "self" and link["rel"] != "album":
                continue
            albums.append(
                    {
                    "HREF": link["href"],
                    "REL": link["rel"],
                    "PATH": link.findPrevious('title').string,
                    }
            )

        parents_by_url = {}
        for index in range(1, len(albums)):
            if albums[index]["REL"] == "album":
                continue

            if index < len(albums) - 1:
                if albums[index + 1]["REL"] == "album":
                    parents_by_url[albums[index]["HREF"]] = albums[index + 1]["HREF"]
                else:
                    parents_by_url[albums[index]["HREF"]] = None
            else:
                parents_by_url[albums[index]["HREF"]] = None

        # all albums to dict
        albums = {}
        for entry in soup('entry'):
            albums[entry.findNext('link', rel="self")['href']] = {
                "URL": entry.findNext('link', rel="self")['href'],
                "PATH": entry.findNext('title').string,
                "COUNT": entry.findNext('f:image-count')["value"],
                "PARENT": parents_by_url[entry.findNext('link', rel="self")['href']]
            }

        # build tree paths
        for key in albums:
            if not albums[key]["PARENT"] is None:
                path = albums[key]["PATH"]
                while 1:
                    parent = albums[key]["PARENT"]
                    path = os.path.join(albums[parent]["PATH"], path)
                    if albums[parent]["PARENT"] == None:
                        break
                    else:
                        albums[key]["PARENT"] = albums[parent]["PARENT"]
                albums[key]["PATH2"] = os.path.join(path)
            else:
                albums[key]["PATH2"] = albums[key]["PATH"]

            print key, albums[key]["PATH2"]


if __name__ == '__main__':
    y = sync_yafotki("yafotkimytest123", "g2h9h4")
    
