from structure import baseModule
from . import download as natsumeDownload
from hentai import Hentai, Format, Option, Sort, Utils

import os
import sys
import requests

class NatsumeHentai(baseModule.BaseModule):
    def __init__(self):
        super().__init__()
        self.dlman = natsumeDownload.NatsumeDownload()

    # your everyday parser
    def parser(self, data: list, mode: str):
        if (mode == "info"): 
            for nuke in data:
                self.hentaiInfo(int(nuke))

        if ("search" in mode): 
            if ('showres' not in mode): 
                self.hentaiSearch(data, mode.split("-")[1])
            else: 
                self.hentaiSearch(data, mode.split("-")[1], res=True)
                
        if (mode == "random"): 
            randSauce = Utils.get_random_id()
            while ("english" not in list(lang.name for lang in Hentai(randSauce).language)):
                randSauce = Utils.get_random_id() 
            self.hentaiInfo(randSauce)
            randOpt = self.utils.verifyOpt("Download?", ["yes", "no", ""])
            if (randOpt == 'yes'): self.hentaiDownload(sauce=[randSauce])
        if (mode == "download"): self.hentaiDownload(sauce=data)

    # to search for a sauce 
    def hentaiSearch(self, data: list, mode: str, res: bool = False) -> int:
        pages = 1
        search = True
        query = None
        for n, tags in enumerate(data): 
            if (" " in tags): data[n] = "\"{}\"".format(tags)
        
        if (mode == 'title'):
            query = " ".join(data)
        elif (mode == 'tags'):
            query = "tag: {}".format(" ".join(data))
        else:
            self.utils.printError("Likely an error occured!")
        # loop in search 
        while (search):
            result = Utils.search_by_query(query, page=pages, sort=Sort.Popular)
            # print(result)
            if (len(result) > 0): 
                if (res):
                    self.utils.printInfo("Founded", str(len(result)))
                    self.utils.printInfo("Pages", str(pages))
                    doujinOpt = [str(x) for x in range(1, len(result)+1)]
                    doujinOpt.append("next")
                    for n, doujin in enumerate(result):
                        self.utils.printInfo("[{:02d}]".format(n+1), doujin.title(format=Format.Pretty))
                        self.utils.printInfo("{:^4}".format("ID"), str(doujin.id))
                    doujinVer = self.utils.verifyOpt("\nChoose doujin or next", doujinOpt)
                    print("")
                    if (doujinVer.isnumeric()):
                        search = False
                        self.hentaiInfo(result[int(doujinVer)-1].id)
                    elif (doujinVer == 'next'):
                        pages+=1
                else:
                    search = False
                    self.hentaiInfo(result[self.utils.getrand(len(result))].id)
                    pass
            else:
                self.utils.printError("No Doujin Found!")
            
        
    # to download a sauce (or sauces)
    def hentaiDownload(self, sauce: list):
        for nuke in sauce:
            nuke = int(nuke)
            if (Hentai.exists(nuke)):
                doujin = Hentai(nuke)
                title = doujin.title(Format.Pretty)
                self.dlman.multiDownloader(doujin.image_urls, type='nhentai', title=title)
                metaFile = os.path.join(self.dlman.downloadFolder, "nhentai", title, "metadata.json")
                doujinOpt = [Option.ID, Option.Title, Option.URL, Option.Tag, Option.Group, Option.Parody, Option.Character, Option.Language, Option.Category, Option.NumPages]
                doujin.export(metaFile, doujinOpt)

    # to get a related info about given sauce
    def hentaiInfo(self, sauce: int) -> int:
        sauce = int(sauce)
        if Hentai.exists(sauce):
            doujin = Hentai(sauce)
            doujinInfo = {}
            doujinInfo['id'] = str(doujin.id)
            doujinInfo['name'] = doujin.title(Format.Pretty)
            doujinInfo['tag'] = list(tag.name for tag in doujin.tag)
            doujinInfo['pages'] = str(doujin.num_pages)
            doujinInfo['author'] = list(artist.name for artist in doujin.artist)
            doujinInfo['lang'] = list(lang.name for lang in doujin.language)
            print("{0}[{1}{2}{0}]{3}".format(self.CMAGENTA, self.CCYAN, doujinInfo['name'], self.CRESET))
            self.utils.printInfo("By", ", ".join(doujinInfo['author']) if len(doujinInfo['author']) != 0 else 'Unknown')
            self.utils.printInfo("Sauce", doujinInfo['id'])
            self.utils.printInfo("tags", ", ".join(doujinInfo['tag']))
            self.utils.printInfo("Language", ", ".join(doujinInfo['lang']))
            self.utils.printInfo("Pages", doujinInfo['pages'])
            sys.stdout.write('\n')
            return sauce
        else:
            self.utils.printError("{} isn't likely a LEGIT sauce".format(str(sauce)))