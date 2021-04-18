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
                            client_id=self.cred["clientID"], client_secret=self.cred["clientSecret"],
                            username=self.cred["username"], password=self.cred["password"]
                            )
        self.cache = dict(list())

    def execute(self, args):
        ctr = 0
        # for post in self.redditClient.subreddit(args[0]).new(limit=None):
        #     with open(os.path.join("cache", "{}.txt".format(post.subreddit)), "a+b") as f:
        #         f.write("[{}] {}\n".format(post.subreddit, post.title).encode("UTF-8"))
        for post in self.redditClient.subreddit(args[0]).new(limit=9999):
            if (str(post.subreddit) not in self.cache.keys()):
                self.cache[str(post.subreddit)] =  dict()

            self.cache[str(post.subreddit)][str(post)] =  {
                    "title": post.title,
                    "url": post.url
            }
            ctr+=1
            sys.stdout.write("Currently processed {} ehm...\r".format(ctr))
        print("...Done!")
        with open("Kyaan.json", "w+") as f:
            json.dump(self.cache, f, indent=3)
