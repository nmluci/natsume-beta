from .utils import NatsumeUtils
import praw
import json, os, sys

class NatsumeRedditAPI():
    def __init__(self):
        self.utils = NatsumeUtils()
        self.cred = self.utils.getConfig()["reddit"]
        self.args = {
            "subreddit": "subreddit, if plural, considers joining it with \"+\" ",
            "limit": "Limits",
        }
        self.redditClient = praw.Reddit(user_agent="nmrika",
                            client_id=self.cred["clientID"], client_secret=self.cred["clientSecret"]
                            )
        self.cache = dict(list())
        self.defaultDir = os.path.join("cache", "reddit.json")

    def getSubredditData(self, subreddit, num):
        if not num: 
            num = "15"
            self.utils.printError("redditAPI", "Limit is set to {}!".format(num))
        try:  
            ctr = 1
            with open(self.defaultDir, "r+") as file:
                if os.stat(self.defaultDir).st_size != 0: 
                    print("Current Filesize: {} kB".format(os.stat(self.defaultDir).st_size//1024))
                    self.cache = json.load(file)

            for post in self.redditClient.subreddit(subreddit).new(limit=num):  
                if (str(post.subreddit) not in self.cache.keys()):
                    self.cache[str(post.subreddit)] = dict()

                sys.stdout.write("[{}] Adding to entries: {}\n".format(ctr, post.title))
                self.cache[str(post.subreddit)][str(post.id)] = {
                    "title": post.title,
                    "url": post.url,
                    "isDownloaded": False
                }
                ctr+=1

            with open(self.defaultDir, "w+") as file:
                json.dump(self.cache, file, indent=4)
        except Exception as e:
            self.utils.printError("RedditAPI", e)

    def getPosts(self, subreddit, num) -> dict:
        self.getSubredditData(subreddit, num)
        subreddit = self.getSubredditName(subreddit)
        if not self.cache[str(subreddit)]:
            self.utils.printError("redditAPI", "Subreddit not yet indexed")
        else:
            try:
                links = list()
                for post in self.cache[subreddit]:
                    temp = self.cache[subreddit][post]
                    links.append(temp["url"])
            except Exception:
                self.utils.printError("reddit", "Failed to fetch posts")
            return links

    def getSubredditName(self, name) -> str:
        for names in self.cache:
            if name == names.lower():
                return names
        self.utils.printError("reddit", "Name not found")
        return name