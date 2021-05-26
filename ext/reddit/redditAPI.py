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
        if not self.cache[str(subreddit)]:
            self.utils.printError("redditAPI", "Subreddit not yet indexed")
        else:
            data = dict()
            data["subreddit"] = self.getSubredditName
            try:
                links = list()
                for post in self.cache[data["subreddit"]]:
                    temp = self.cache[data["subreddit"]][post]
                    links.append(temp["url"])
            except Exception:
                pass

            data["urls"] = links
            return data

    def getSubredditName(self, name) -> str:
        for names in self.cache:
            if name == names.lower():
                return names
        self.utils.printError("reddit", "Name not found")
        return name