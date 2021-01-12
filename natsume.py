from imgur_python import Imgur
from bs4 import BeautifulSoup
from hentai import Hentai, Format, Utils, Sort, Option
import pathlib
import traceback
import modules.utils as natsumeUtils
import modules.reddit as natsumeReddit
import modules.imgur as natsumeImgur
import youtube_dl
import praw
import requests
import urllib
import signal
import os
import sys
import json
import time

class NatsumeAI:
    def __init__(self, debug=False):
        self.utils = natsumeUtils.NatsumeUtils()

        self.CRED = self.utils.CRED
        self.CCYAN = self.utils.CCYAN
        self.CXMAGENTA = self.utils.CXMAGENTA
        self.CMAGENTA = self.utils.CMAGENTA
        self.CRESET = self.utils.CRESET

        self.downloadFolder = 'Download'
        self.state = True
        self.isExiting = False
        self.isDebug = "False" if not debug else "True"
        self.isDownNH = False
        self.ignoredCount = 0
        self.dlCount = 0

        if os.path.isfile("config.fyn"):
            with open("config.fyn") as f:
                data = json.load(f)
                self.reddit = list()
                self.reddit.append(data['Reddit']["clientID"])
                self.reddit.append(data['Reddit']["clientSecret"])
                self.reddit.append(data['Reddit']["username"])
                self.reddit.append(data['Reddit']["password"])
                self.redditParser = natsumeReddit.NatsumeReddit(self.reddit)
                self.imgurParser = natsumeImgur.NatsumeImgur()

        else:
            print("{}NO CONFIG FOUND!!!{}".format(self.CXMAGENTA, self.CRESET))
            exit()
        
        self.title = ""
        self.submodule = 0
        self.VER = "2.2"
        self.CHUNK = 2**15
        # signal.signal(signal.SIGTERM, self.graceExit)
        # signal.signal(signal.SIGINT, self.graceExit)

        sys.stdout.write('{}Natsume AI v{:s} {}{} {}\n\n'.format(self.CXMAGENTA, self.VER, self.CCYAN,"<Debugging Mode>" if debug else "", self.CRESET))

        self.argsParsed(self.utils.argsParser())

    def argsParsed(self, args: list):
        self.submodule = args.submodule
        if self.submodule == 'reddit':
            if (args.i): 
                self.redditParser.parser(args.subreddit, args.n, ignored=True)
            else: 
                self.redditParser.parser(args.subreddit, args.n)
        if self.submodule == 'nhentai':
            self.nhParser(args.sauce, True if args.dl else False)
        if self.submodule == 'imgur':
            self.imgurParser.parser(args.url, 'imgur')
        if self.submodule == 'ph':
            pass
        if self.submodule == 'auto':
            pass
        if self.submodule == None:
            self.utils.printError("No Argument Given!!")
    
    def nhUtilsParser(self, search, mode):
        pass

    def nhParser(self, sauce, dl: bool):
        for nuke in sauce:
            nuke = int(nuke)
            if (Hentai.exists(nuke)):
                doujin = Hentai(nuke)
                title = doujin.title(Format.Pretty)
                # title = str(nuke)
                # print(title)
                self.multiDownloader(doujin.image_urls, 'nh', title)
                self.isDownNH = False
                metaFile = os.path.join(self.downloadFolder, title, "metadata.json")
                doujinOpt = [Option.ID, Option.Title, Option.URL, Option.Tag, Option.Group, Option.Parody, Option.Character, Option.Language, Option.Category, Option.NumPages]
                doujin.export(metaFile, doujinOpt)

    def debugStats(self, print=False):
        if print:
            sys.stdout.write("{}<<DEBUG STATE: {}{}{}>>{}".format(self.CXMAGENTA, self.CCYAN, self.isDebug, self.CXMAGENTA, self.CRESET))
        else:
            return self.isDebug
        
    def graceExit(self, signum=None, frame=None):
        self.state = False
        if self.isExiting:
            print("{}Exiting...{}".format(self.CRED, self.CRESET))
            exit()
    
    def clearScreen(self):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')