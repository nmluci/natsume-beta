from structure import extensions
import requests, json, os, sys

class NatsumeRedditAPI(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "redditman"
        self.desc = "Master's own implementations of Reddit API using Reddit's own public API"
        self.help = "Wha! Nothing to see here!"
        self.isSystem = True
        
    def execute(self, args):
        data = requests.get("https://www.reddit.com/r/hentai/new.json?limit=10")
        with open("Fyn.txt", "a+") as f:
            json.dump(data.json(), fp=f, indent=4)
            print("Done~")