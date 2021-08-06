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
                "default": 5
            },
            {
                "name": "download",
                "type": bool,
                "default": False 
            }
        ]
        self.alias = [self.name.lower()]
        self.isSystem = False
        self.reddit = NatsumeRedditAPI()
        self.download = ExtDownloader()
        
    def execute(self, subreddit, sum, download):
        try:
           urls = self.reddit.getPosts(subreddit, sum)
           if download: self.download.downloader(urls, "reddit")
        except Exception as e:
            self.utils.printError("Reddit Downloader", e)