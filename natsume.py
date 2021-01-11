from imgur_python import Imgur
from bs4 import BeautifulSoup
from hentai import Hentai, Format, Utils, Sort, Option
import pathlib
import traceback
import modules.utils as natsumeUtils
import youtube_dl
import praw
import requests
import urllib
import signal
import os
import sys
import json
import time

class NatsumeAI:
    def __init__(self, debug=False, ignore=False):
        self.utils = natsumeUtils.NatsumeUtils()

        self.CRED = self.utils.CRED
        self.CCYAN = self.utils.CCYAN
        self.CXMAGENTA = self.utils.CXMAGENTA
        self.CMAGENTA = self.utils.CMAGENTA
        self.CRESET = self.utils.CRESET

        self.downloadFolder = 'Download'
        self.state = True
        self.isExiting = False
        self.isDebug = "False" if not debug else "True"
        self.isDownNH = False
        self.isIgnored = ignore
        self.ignoredCount = 0
        self.dlCount = 0
        if os.path.isfile("config.fyn"):
            with open("config.fyn") as f:
                data = json.load(f)
                self.imgur = list()
                self.reddit = list()
                self.imgur.append(data['Imgur']['clientID'])
                self.imgur.append(data['Imgur']['clientSecret'])
                self.reddit.append(data['Reddit']["clientID"])
                self.reddit.append(data['Reddit']["clientSecret"])
                self.reddit.append(data['Reddit']["username"])
                self.reddit.append(data['Reddit']["password"])
        else:
            print("{}NO CONFIG FOUND!!!{}".format(self.CXMAGENTA, self.CRESET))
            exit()
        
        self.title = ""
        self.submodule = 0
        self.VER = "2.0"
        self.CHUNK = 2**15
        self.session = requests.Session()
        signal.signal(signal.SIGTERM, self.graceExit)
        signal.signal(signal.SIGINT, self.graceExit)

        sys.stdout.write('{}Natsume AI v{:s} {}{} {}\n\n'.format(self.CXMAGENTA, self.VER, self.CCYAN,"<Debugging Mode>" if debug else "", self.CRESET))

        self.argsParsed(self.utils.argsParser())

    def argsParsed(self, args: list):
        self.submodule = args.submodule
        if self.submodule == 'reddit':
            if (args.i): self.isIgnored = True
            self.redditParser(args.subreddit, args.n)

        if self.submodule == 'nhentai':
            self.nhParser(args.sauce)
        if self.submodule == 'imgur':
            self.imgurParser(args.url)
        if self.submodule == 'ph':
            pass
        if self.submodule == 'auto':
            pass
        if self.submodule == None:
            self.utils.printError("No Argument Given!!")
    
    def nhUtilsParser(self, search, mode):
        pass

    def nhParser(self, sauce):
        for nuke in sauce:
            nuke = int(nuke)
            if (Hentai.exists(nuke)):
                doujin = Hentai(nuke)
                title = doujin.title(Format.Pretty)
                # title = str(nuke)
                # print(title)
                self.multiDownloader(doujin.image_urls, 'nh', title)
                self.isDownNH = False
                metaFile = os.path.join(self.downloadFolder, title, "metadata.json")
                doujinOpt = [Option.ID, Option.Title, Option.URL, Option.Tag, Option.Group, Option.Parody, Option.Character, Option.Language, Option.Category, Option.NumPages]
                doujin.export(metaFile, doujinOpt)

    def redditParser(self, subreddit: str, count: int, standalone: bool = True):
        if standalone:
            sys.stdout.write("{}Subreddit: {}r/{} {}\n".format(self.CCYAN, self.CRED, subreddit, self.CRESET))
            sys.stdout.write("{}Count: {}{} {} {}\n\n".format(self.CCYAN, self.CRED, count, "[+]" if self.isIgnored else "", self.CRESET))

        r = praw.Reddit(user_agent="nmrika", client_id= self.reddit[0], client_secret= self.reddit[1], username=self.reddit[2], password=self.reddit[3])
        if (self.isIgnored): 
            for post in r.subreddit(subreddit).new(limit=None):
                if (count == self.dlCount): self.graceExit()
                if "i.redd.it" in post.url:
                    self.title = post.title
                    url = post.url
                    filename = os.path.join(subreddit, post.url.split('/')[len(post.url.split('/'))-1])
                    self.download(url, filename, self.title)

                if "imgur.com" in post.url:
                    self.title = post.title
                    self.imgurParser(post.url, subreddit)

                if "redgifs.com" in post.url:
                    self.title = str(post.title)
                    filename = os.path.join(subreddit, post.url.split('/')[len(post.url.split('/'))-1])

                    if ".webm" in post.url or '.mp4' in post.url or '.gif' in post.url:
                        self.download(post.url, filename, self.title)
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

                            filename = os.path.join(subreddit, url.split('/')[len(url.split("/"))-1])
                            self.download(url, filename, self.title)
                        except Exception as e:
                            traceback.print_exc()
                            sys.stdout.write("{}[ERROR] {}{}\n".format(self.CXMAGENTA, e, self.CRESET))
                            pass

        for post in r.subreddit(subreddit).new(limit=count):
            if "redgifs.com" in post.url:
                self.title = str(post.title)
                filename = os.path.join(subreddit, post.url.split('/')[len(post.url.split('/'))-1])

                if ".webm" in post.url or '.mp4' in post.url or '.gif' in post.url:
                    self.download(post.url, filename, self.title)
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

                        filename = os.path.join(subreddit, url.split('/')[len(url.split("/"))-1])
                        self.download(url, filename, self.title)
                    except Exception as e:
                        traceback.print_exc()
                        sys.stdout.write("{}[ERROR] {}{}\n".format(self.CXMAGENTA, e, self.CRESET))
                        pass                
                
            if "i.redd.it" in post.url:
                self.title = post.title
                url = post.url
                filename = os.path.join(subreddit, post.url.split('/')[len(post.url.split('/'))-1])
                self.download(url, filename, self.title)

            if "imgur.com" in post.url:
                self.title = post.title
                self.imgurParser(post.url, subreddit)

    def debugStats(self, print=False):
        if print:
            sys.stdout.write("{}<<DEBUG STATE: {}{}{}>>{}".format(self.CXMAGENTA, self.CCYAN, self.isDebug, self.CXMAGENTA, self.CRESET))
        else:
            return self.isDebug
        
    def graceExit(self, signum=None, frame=None):
        self.state = False
        if self.isExiting:
            print("{}Exiting...{}".format(self.CRED, self.CRESET))
            exit()
    
    def clearScreen(self):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')

    def imgurParser(self, url, src=None):
        imgurClient = Imgur({'client_id': self.imgur[0]})

        if src != None:
            filename = os.path.join(src, url.split('/')[len(url.split('/'))-1])
        else:
            filename = os.path.join('Imgur', url.split('/')[len(url.split('/'))-1])

        try:
            if "/a/" in url:
                albumId = url.split('/')[len(url.split('/'))-1]
                urlList = imgurClient.album_images(albumId)
                title = "Album {}".format(albumId)
                self.multiDownloader(urlList, 'Imgur', title)
            else:
                self.download(url, filename, self.title)
        except Exception as e:
            import traceback
            traceback.print_exc()
            sys.stdout.write("{}[ERROR] {}{}".format(self.CXMAGENTA, e, self.CRESET))

    def multiDownloader(self, data, type=None, title=None):
        title = title if title is not None else ""
        if type == 'Imgur':
            for url in data['response']['data']:
                url = url['link']
                filename = os.path.join(title, url.split("/")[len(url.split("/"))-1])
                self.bulkDownloader(url, filename, title, src='imgur')

        if type == 'nh':
            title = str(title)
            self.bulkDownloader(data, title, src='nh')

    def bulkDownloader(self, data, title="", src=None):
        progress = 0
        baseFolder = self.downloadFolder
        bulkSize = len(data)
        if src == 'nh': src = 'nhentai'
        if src == 'imgur': src = 'Imgur'

        for url in data:
            try:
                if not self.state:
                    print("\n{}Starting Exit Procedure...{}".format(self.CXMAGENTA, self.CRESET))
                    self.isExiting = True
                    self.graceExit()
                response = self.session.head(url)
                if response.status_code == 200:
                    fSize = int(response.headers.get("Content-Length"))
                    response = self.session.get(url, stream=True)
                    filename = os.path.join(title, url.split("/")[len(url.split("/"))-1])
                    
                    dlPath = os.path.join(baseFolder, src, filename)
                    if not os.path.isdir(os.path.split(dlPath)[0]):
                        os.makedirs(os.path.split(dlPath)[0])

                    if os.path.isfile(dlPath) and os.stat(dlPath).st_size == fSize:
                        progress += 1
                        sys.stdout.write("{}[E] {:s} Downloading [{:3d}/{:3d}] {}\r".format(
                                self.CXMAGENTA, title, progress, bulkSize, self.CRESET
                        ))
                    else:
                        with open(dlPath, "wb") as f:
                            progress += 1
                            f.write(response.content)
                            sys.stdout.write("{}[D] {:s} Downloading [{:3d}/{:3d}] {}\r".format(
                                self.CCYAN, title, progress, bulkSize, self.CRESET
                            ))
                            # self.clearScreen()
            except Exception as e:
                traceback.print_exc()
                sys.stdout.write("{}[Error] {}{}\n".format(self.CMAGENTA, e, self.CRESET))
        self.clearScreen()
        sys.stdout.write("{}[E] {} {} Files Downloaded {}\n".format(
            self.CXMAGENTA, title, bulkSize, self.CRESET
        ))
        
    def download(self, url, filename, title=None, src='reddit'):
        progress = 0
        baseFolder = self.downloadFolder

        if len(title) >= 53:
            if title is not None:
                title = title[:25] + "..." if len(str(os.path.split(filename)[1])) >= 28 else title[:50] + "..."
        if src == 'nh':
            if not self.isDownNH:
                self.utils.printInfo('Sauce', title)
            title = ""
            self.isDownNH = True

        try:
            if not self.state:
                print("{}Starting Exit Procedure...{}".format(self.CXMAGENTA, self.CRESET))
                self.isExiting = True
                self.graceExit()
            response = self.session.head(url)
            if len(title) > 50: title = str(title[:50] + '...')     
            if response.status_code == 200:
                fSize = int(response.headers.get("Content-Length"))
                response = self.session.get(url, stream=True)

                dlPath = os.path.join(baseFolder, src, filename)
                if not os.path.isdir(os.path.split(dlPath)[0]):
                    os.makedirs(os.path.split(dlPath)[0])

                if os.path.isfile(dlPath) and os.stat(dlPath).st_size == fSize:
                    if (self.isIgnored): self.ignoredCount += 1
                    print("{}[E] {} {:.2f}MB {} {:s}".format(
                        self.CRED, os.path.split(filename)[1], (os.stat(dlPath).st_size/2**20), self.CRESET, title if title != None else " "
                    ))
                else:
                    with open(dlPath, "wb") as f:
                        for chunk in response.iter_content(self.CHUNK):
                            progress += self.CHUNK
                            f.write(chunk)
                            sys.stdout.write("{}[D] {:s} Downloading {:.2f} MB... ({:.2f}%) [{:s}]{}\r".format(
                                self.CCYAN, os.path.split(filename)[1], float(fSize/2**20), (progress/fSize*100 if progress/fSize*100 <= 100 else 100), title if title != None else " ", self.CRESET
                            ))
                            time.sleep(.01)
                    if (self.isIgnored): self.dlCount += 1
                    self.clearScreen()
                    sys.stdout.write("{}[E] {} {:.2f} MB {} {:s}\n".format(
                        self.CXMAGENTA, os.path.split(filename)[1], float(os.stat(dlPath).st_size/2**20), self.CRESET, title if title != None else " "
                    ))

        except Exception as e:
            sys.stdout.write("{}[ERROR] {}{}\n".format(self.CXMAGENTA, e, self.CRESET))