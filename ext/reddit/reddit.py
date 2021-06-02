from . import redditAPI
import os, json, sys

class NatsumeRedditDownloader(redditAPI.NatsumeRedditAPI):
    def __init__(self, main):
        super().__init__(main)
        self.name = "Reddit Downloader"
        self.args = {
            "subreddit": "subreddit, if plural, considers joining it with \"+\"",
            "sum": "limits",
            "download": "toggle download or not"
        }
        self.isSystem = False

    def execute(self, args):
        if len(args) != 2:
            self.utils.printError("Reddit Downloader", "Sum Not Specified!")
            args.append(15)
        try:
           urls = self.getPosts(args[0], int(args[1]))
        #    for url in urls:
        #        print(url) 
        except Exception as e:
            self.utils.printError("Reddit Downloader", e)
