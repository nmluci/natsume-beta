
from structure.download import NatsumeDownloader
from structure.redditAPI import NatsumeRedditAPI
from structure.extensions import NatsumeExt
import os, json, sys

class NatsumeRedditDownloader(NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "Reddit Downloader"
        self.args = {
            "subreddit": "subreddit, if plural, considers joining it with \"+\"",
            "sum": "limits",
            "download": "toggle download or not"
        }
        self.isSystem = False
        self.reddit = NatsumeRedditAPI()
        self.download = NatsumeDownloader()
        
    def execute(self, args):
        if len(args) != 2:
            self.utils.printError("Reddit Downloader", "Sum Not Specified!")
            args.append(15)
        try:
           urls = self.getPosts(args[0], int(args[1]))
           self.download.downloader(urls, "reddit")
        except Exception as e:
            self.utils.printError("Reddit Downloader", e)

