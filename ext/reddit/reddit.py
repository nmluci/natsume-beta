from structure.download import ExtDownloader
from structure.redditAPI import NatsumeRedditAPI
from structure import extensions
import os, json, sys

class NatsumeRedditDownloader(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "Reddit"
        self.args = [
            {
                "name": "subreddit"
            },
            {
                "name": "sum",
                "type": int,
            },
            {
                "name": "download",
                "optional": True
            }
        ]
        self.alias = [self.name.lower()]
        self.isSystem = False
        self.reddit = NatsumeRedditAPI()
        self.download = ExtDownloader()
        
    def execute(self, args):
        if len(args) != 2:
            self.utils.printError("Reddit Downloader", "Sum Not Specified!")
            args.append(15)
        try:
           urls = self.reddit.getPosts(args[0], int(args[1]))
           self.download.downloader(urls, "reddit")
        except Exception as e:
            self.utils.printError("Reddit Downloader", e)

    def menu(self):
        pass