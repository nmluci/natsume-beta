from structure import baseModule
from . import download as natsumeDownload
from imgur_python import Imgur
import os
import sys
import json

class NatsumeImgur(baseModule.BaseModule):
    def __init__(self):
        super().__init__()
        self.dlman = natsumeDownload.NatsumeDownload()
        
    def parser(self, url, title=None, src=None):
        if src == None: self.utils.printError("Invalid Source!")
        imgurClient = Imgur({'client_id': self.imgur[0]})

        filename = os.path.join(url.split('/')[len(url.split('/'))-1])
        
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