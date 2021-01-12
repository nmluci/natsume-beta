from imgur_python import Imgur
from . import download as natsumeDownload
from . import utils as natsumeUtils
import os
import sys
import json

class NatsumeImgur:
    def __init__(self):
        self.dlman = natsumeDownload.NatsumeDownload()
        self.utils = natsumeUtils.NatsumeUtils()

        self.CRED = self.utils.CRED
        self.CCYAN = self.utils.CCYAN
        self.CXMAGENTA = self.utils.CXMAGENTA
        self.CMAGENTA = self.utils.CMAGENTA
        self.CRESET = self.utils.CRESET

        self.imgur = list()
        with open("././config.fyn") as f:
            data = json.load(f)
            self.imgur.append(data['Imgur']['clientID'])

    def parser(self, url, title=None, src=None):
        if src == None: self.utils.printError("Invalid Source!")
        imgurClient = Imgur({'client_id': self.imgur[0]})

        if src == 'imgur':
            filename = os.path.join(src, url.split('/')[len(url.split('/'))-1])
        else:
            filename = os.path.join(src, url.split('/')[len(url.split('/'))-1])

        try:
            if "/a/" in url:
                albumId = url.split('/')[len(url.split('/'))-1]
                urlList = imgurClient.album_images(albumId)
                title = "Album {}".format(albumId)
                self.dlman.multiDownloader(urlList, 'imgur', title)
            elif src == 'imgur':
                self.dlman.download(url, filename, title, src='imgur')
            else:
                self.dlman.download(url, filename, title, src='reddit')
        except Exception as e:
            sys.stdout.write("{}[ERROR] {}{}".format(self.CXMAGENTA, e, self.CRESET))