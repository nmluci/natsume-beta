import os, sys
from pathlib import Path
from multiprocessing.pool import ThreadPool

import requests
from . import utils

class NatsumeDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.__downloadFolder = "Tmp"
        self.CHUNK = 2048
        self.utils = utils.NatsumeUtils()        
        self.src = None

    def downloader(self, urls: list, src: str = None, worker: int = 5):
        if src == None: src = "misc"
        self.src = src
        res = ThreadPool(worker).imap_unordered(self.downloaderCore, urls)

        if -1 in res:
            print("Some failed to downloaded!")

    def downloaderCore(self, url: str):
        try:
            if self.src.lower() == "nhentai":
                dlPath = Path(self.__downloadFolder, self.src, url.split("/")[-2])
            else:
                dlPath = Path(self.__downloadFolder, self.src)

            if not dlPath.is_dir(): dlPath.mkdir(parents=True, exist_ok=True)
            filename = dlPath.joinpath(url.split("/")[-1])
            response = self.session.head(url)
            fSize = int(response.headers.get("Content-Length"))
            if fSize == None: 
                fSize = 1
            else:
                if filename.is_file() and filename.stat().st_size == fSize: pass
            
            if response.status_code != 200:
                raise requests.HTTPError("Url not found!")
            
            response = self.session.get(url, stream=True)

            with open(filename, "wb+") as file:
                for chunk in response.iter_content(self.CHUNK):
                    file.write(chunk)
            return 0
        except Exception:
            self.utils.printError("DL", f"{dlPath}\n")
            return -1