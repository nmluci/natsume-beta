from re import template
from . import utils as natsumeUtils
import os
import sys
import time
import traceback
import requests
import signal

class NatsumeDownload:
    def __init__(self):
        self.utils = natsumeUtils.NatsumeUtils()
        
        self.CRED = self.utils.CRED
        self.CCYAN = self.utils.CCYAN
        self.CXMAGENTA = self.utils.CXMAGENTA
        self.CMAGENTA = self.utils.CMAGENTA
        self.CRESET = self.utils.CRESET

        self.session = requests.Session()
        self.downloadFolder = 'Download'
        self.state = True
        self.isExiting = False
        self.CHUNK = 2**15
        signal.signal(signal.SIGTERM, self.utils.graceExit)
        signal.signal(signal.SIGINT, self.utils.graceExit)
            
    def clearScreen(self):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')
        
    def multiDownloader(self, data, type=None, title=None):
        title = title if title is not None else ""
        if type == 'imgur':
            for url in data['response']['data']:
                url = url['link']
                # filename = os.path.join(title, url.split("/")[len(url.split("/"))-1])
                self.dlman.bulkDownloader(url, title, src='imgur')

        if type == 'nhentai':
            title = str(title)
            self.dlman.bulkDownloader(data, title, src='nhentai')

    def bulkDownloader(self, data: list, title=None, src=None):
        progress = 0
        baseFolder = self.downloadFolder
        bulkSize = len(data)

        for url in data:
            try:
                if not self.state:
                    print("{}Starting Exit Procedure...{}".format(self.CXMAGENTA, self.CRESET))
                    self.isExiting = True
                    self.utils.graceExit()
                response = self.session.head(url)
                if response.status_code == 200:
                    fSize = int(response.headers.get("Content-Length"))
                    response = self.session.get(url, stream=True)
                    filename = os.path.join(title, url.split("/")[len(url.split("/"))-1])

                    dlPath = os.path.join(baseFolder, src, filename)
                    if not os.path.isdir(os.path.split(dlPath)[0]):
                        os.makedirs(os.path.split(dlPath)[0])
                    
                    if os.path.isfile(dlPath) and os.stat(dlPath).st_size == fSize:
                        progress += 1
                        sys.stdout.write("{}[E] {:s} Downloading [{:3d}/{:3d}] {}\r".format(
                            self.CXMAGENTA, title, progress, bulkSize, self.CRESET
                        ))
                    else:
                        with open(dlPath, "wb") as f:
                            progress += 1
                            sys.stdout.write("{}[D] {:s} Downloading [{:3d}/{:3d}] {}\r".format(
                                self.CCYAN, title, progress, bulkSize, self.CRESET
                            ))
                            for chunk in response.iter_content(self.CHUNK):
                                f.write(chunk)
            except Exception as e:
                traceback.print_exc()
                self.utils.printError(e)

        self.clearScreen()
        sys.stdout.write("{}[E] {} {} Files Downloaded {}\n".format(
            self.CXMAGENTA, title, bulkSize, self.CRESET
        ))

    def download(self, url, filename, title=None, src=None, ignore=False):
        progress = 0
        baseFolder = self.downloadFolder

        if len(title) >= 53:
            if title is not None:
                title = title[:25] + "..." if len(str(os.path.split(filename)[1])) >= 28 else title[:50] + "..."
        
        try:
            if not self.state:
                print("{}Starting Exit Procedure...{}".format(self.CXMAGENTA, self.CRESET))
                self.isExiting = True
                self.utils.graceExit()
            
            response = self.session.head(url)
            if response.status_code == 200:
                fSize = int(response.headers.get("Content-Length"))
                response = self.session.get(url, stream=True)

                dlPath = os.path.join(baseFolder, src, filename)
                if not os.path.isdir(os.path.split(dlPath)[0]):
                    os.makedirs(os.path.split(dlPath)[0])
                
                if os.path.isfile(dlPath) and os.stat(dlPath).st_size == fSize:
                    sys.stdout.write("{}[E] {} {:.2f}MB {} {:s}\n".format(
                        self.CRED, os.path.split(filename)[1], (os.stat(dlPath).st_size/2**20), self.CRESET, title if title != None else ""
                    ))
                    if ignore: return False
                else:
                    with open(dlPath, "wb") as f:
                        for chunk in response.iter_content(self.CHUNK):
                            progress += self.CHUNK
                            f.write(chunk)
                            sys.stdout.write("{}[D] {:s} Downloading {:.2f}MB... ({:.2f}%) [{:s}]\r".format(
                                self.CCYAN, os.path.split(filename)[1], float(fSize/2**20), (progress/fSize*100 if progress/fSize*100 <= 100 else 100), title if title != None else "", self.CRESET
                            ))
                            time.sleep(.01)
                    self.clearScreen()
                    sys.stdout.write("{}[E] {} {:.2f}MB {} {:s}\n".format(
                        self.CXMAGENTA, os.path.split(filename)[1], float(os.stat(dlPath).st_size/2**20), self.CRESET, title if title != None else ""
                    ))
                    if (ignore): return True
        except Exception as e:
            self.utils.printError(e)


                    