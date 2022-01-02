from structure.download import ExtDownloader
from structure.redditAPI import NatsumeRedditAPI
from structure import extensions
import os, json, sys

class NatsumeRedditDownloader(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Reddit"
        self.args = [
            {
                "name": "subreddit"
            },
            {
                "name": "sum",
                "type": int,
                "optional": True,
                "default": 5
            },
            {
                "name": "download",
                "type": bool,
                "optional": True,
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