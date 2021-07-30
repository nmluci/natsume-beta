from __future__ import annotations
from typing import List

import os, sys
from pathlib import Path
from multiprocessing.pool import ThreadPool

import requests
from . import utils

class ExtDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.__downloadFolder = "download"
        self.CHUNK = 2048
        self.utils = utils.NatsumeUtils()        
        self.src = None

    def downloader(self, urls: list, src: str = None, worker: int = 5):
        if src == None: src = "misc"
        self.src = src
        res = ThreadPool(worker).imap(self.downloaderCore, urls)

        if -1 in res:
            print("Some failed to downloaded!")

    def downloadPartial(self, url: str, src: str=None, worker: int = 5, chunk: int = 2**25):
        try:
            self.src = src
                
            head = self.session.head(url)
            isPartialSupported = head.headers.get("Accept-Ranges")
            if not isPartialSupported:
                raise ValueError("This URL doesn't support partial download!")


            fSize = int(head.headers.get("Content-Length"))

            chunkCount = (fSize//chunk)
            chunkList = []

            for num, ctr in enumerate(range(chunkCount)):
                chunkList.append([num, url, chunk*ctr, chunk*(ctr+1)-1])
            
            result = ThreadPool(worker).imap_unordered(self.downloadPartialCore, chunkList)
            if result != 0:
                self.utils.printError("partialDL", "An error might occured during the process!")
        except Exception as e:
            self.utils.printError("dlPartial", f"Another Exception Occured: {e}")

    def downloadPartialCore(self, metadata: List[int, str, int, int]):
        try:
            num = metadata[0]
            url = metadata[1]
            start = metadata[2]
            end = metadata[3]
            
            dlPath = Path(self.__downloadFolder, self.src)
            if not dlPath.is_dir(): dlPath.mkdir(parents=True, exist_ok=True)

            partialData = self.session.get(
                url= url,
                headers= {
                    "Range": f"bytes={start}-{end}"
                },
                stream=True
            )

            if not partialData:
                raise ValueError("Invalid URL!")
            
            filename:str = f'{url.split("/")[-1].split("?")[0]}.part{num}'

            with open(filename, "wb+") as file:
                for chunk in partialData.iter_content(self.CHUNK):
                    file.write(chunk)
            self.utils.printInfo("partialDL", f"{filename} Downloaded!")
            return 0
        except Exception as e:
            self.utils.printError("partialDL", f"Another Exception Occured: {e}")
            return 1

    def downloaderCore(self, url: str):
        try:
            if self.src.split("-")[0] == "nhentai":
                dlPath = Path(self.__downloadFolder, "nhentai", self.src.split("-")[1])
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
        except Exception as e:
            self.utils.printError("DL", e)
            return -1
        else:
            self.utils.printInfo("DL", f"{filename} downloaded!")
            return 0
