from inspect import indentsize
from structure import extensions
import praw
import json, os, sys

class NatsumeRedditAPI(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "redditman"
        self.desc = "Master's own implementations of Reddit API using Reddit's own public API"
        self.help = "Wha! Nothing to see here!"
        self.isSystem = True
        self.cred = self.base.settings["reddit"]
        self.args = {
            "subreddit": "subreddit, if plural, considers joining it with \"+\" ",
            "sort": "Sorting (New/Top)",
            "limit": "Limits"
        }
        self.redditClient = praw.Reddit(user_agent="nmrika",
                            client_id=self.cred["clientID"], client_secret=self.cred["clientSecret"]
                            )
        self.cache = dict(list())

    def execute(self, args):
        if len(args) == 0: 
            self.utils.printError("reddit", "no args!")
            return -1
        ctr = 0
        
        file = open("fua.json", "w+")
        if os.stat("Fua.json").st_size != 0: 
            print(os.stat("Fua.json").st_size)
            self.cache = json.load(file)
            print(json.dumps(self.cache, indent=4))
        
        for post in self.redditClient.subreddit(args[0]).new(limit=10):
            if (str(post.subreddit) not in self.cache.keys()):
                sys.stdout.write("[{}] Adding to entries {}\n".format(ctr, post.title))
                self.cache[str(post.subreddit)] = dict()

            self.cache[str(post.subreddit)][str(post)] = {
                "title": post.title,
                "url": post.url
            }
            ctr+=1
        
        json.dump(self.cache, file, indent=3)
        print(json.dumps(self.cache, indent=3))
        file.close()