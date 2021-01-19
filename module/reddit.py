from . import imgur
from . import download as natsumeDownload

from bs4 import BeautifulSoup
from structure import baseModule
import urllib
import praw
import sys
import os
import json

class NatsumeReddit(baseModule.BaseModule):
    def __init__(self):
        super().__init__()
        self.imgurMan = imgur.NatsumeImgur()
        self.dlman = natsumeDownload.NatsumeDownload()
        self.dlCount = 0

    def parser(self, subreddit: list, count: int, ignored=False):
        sys.stdout.write("{}Subreddit: {}r/{} {}\n".format(self.CCYAN, self.CRED, " r/".join(subreddit), self.CRESET))
        sys.stdout.write("{}Count: {}{} {} {}\n\n".format(self.CCYAN, self.CRED, count, "[+]" if ignored else "", self.CRESET))

        r = praw.Reddit(user_agent="nmrika", client_id= self.reddit[0], client_secret= self.reddit[1], username=self.reddit[2], password=self.reddit[3])
        subreddit = "+".join(subreddit)
        if (ignored): 
            for post in r.subreddit(subreddit).new(limit=None):
                if (count <= self.dlCount): self.utils.graceExit()
                if "i.redd.it" in post.url:
                    self.title = post.title
                    url = post.url
                    filename = os.path.join(post.url.split('/')[len(post.url.split('/'))-1])
                    res = self.dlman.download(url, filename, self.title, src="reddit", ignore=True)
                    if (res): self.dlCount += 1

                if "imgur.com" in post.url:
                    self.title = post.title
                    self.imgurMan.parser(post.url, title=self.title, src=subreddit)
                    self.dlCount += 1

                if "redgifs.com" in post.url:
                    self.title = str(post.title)
                    filename = os.path.join(post.url.split('/')[len(post.url.split('/'))-1])

                    if ".webm" in post.url or '.mp4' in post.url or '.gif' in post.url:
                        res = self.dlman.download(post.url, filename, self.title, src="reddit", ignore=True)
                        if res: self.dlCount += 1
                    else:
                        try:
                            url = post.url
                            if url[:-1] == "/":
                                url = post.url[:-1]
                        
                            url = "https://www.redgifs.com/watch/{}".format(url.split('/')[len(url.split('/'))-1])
                            
                            pageSource = urllib.request.urlopen(url).read().decode()

                            soup = BeautifulSoup(pageSource, "html.parser")
                            attrib = {"data-react-helmet": "true", "type": "application/ld+json"}
                            content = soup.find("script", attrs=attrib)

                            if content is None:
                                print("{}Error{}".format(self.CXMAGENTA, self.CRESET))
                        
                            url = json.loads(content.contents[0])["video"]["contentUrl"]

                            filename = os.path.join(url.split('/')[len(url.split("/"))-1])
                            res = self.dlman.download(url, filename, self.title, src="reddit", ignore=True)
                            if (res): self.dlCount += 1
                        except Exception as e:
                            sys.stdout.write("{}[ERROR] {}{}\n".format(self.CXMAGENTA, e, self.CRESET))
                            pass

        for post in r.subreddit(subreddit).new(limit=count):
            if "redgifs.com" in post.url:
                self.title = str(post.title)
                filename = os.path.join(post.url.split('/')[len(post.url.split('/'))-1])

                if ".webm" in post.url or '.mp4' in post.url or '.gif' in post.url:
                    self.dlman.download(post.url, filename, self.title, src="reddit")
                else:
                    try:
                        url = post.url
                        if url[:-1] == "/":
                            url = post.url[:-1]
                    
                        url = "https://www.redgifs.com/watch/{}".format(url.split('/')[len(url.split('/'))-1])
                        
                        pageSource = urllib.request.urlopen(url).read().decode()

                        soup = BeautifulSoup(pageSource, "html.parser")
                        attrib = {"data-react-helmet": "true", "type": "application/ld+json"}
                        content = soup.find("script", attrs=attrib)

                        if content is None:
                            print("{}Error{}".format(self.CXMAGENTA, self.CRESET))
                    
                        url = json.loads(content.contents[0])["video"]["contentUrl"]

                        filename = os.path.join(url.split('/')[len(url.split("/"))-1])
                        self.dlman.download(url, filename, self.title, src="reddit")
                    except Exception as e:
                        sys.stdout.write("{}[ERROR] {}{}\n".format(self.CXMAGENTA, e, self.CRESET))
                        pass                

            if "imgur.com" in post.url:
                self.title = post.title
                self.imgurMan.parser(post.url, self.title, subreddit)

            if "imgur.com" not in post.url:
                self.title = post.title
                if ".jpg" or "png" in post.url.split('/')[len(post.url.split('/'))-1]:
                    url = post.url
                    filename = os.path.join(post.url.split('/')[len(post.url.split('/'))-1])
                    self.dlman.download(url, filename, self.title, src="reddit")