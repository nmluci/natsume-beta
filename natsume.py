import structure.utils as natsumeUtils
import module.nhentai as nhentai
import module.imgur as imgur
import module.reddit as reddit
import module.anilist as anilist
import sys

class NatsumeAI:
    def __init__(self, debug=False):
        self.hentai = nhentai.NatsumeHentai()
        self.imgurParser = imgur.NatsumeImgur()
        self.redditParser = reddit.NatsumeReddit()
        self.animeParser = anilist.NatsumeAniList()
        
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
        self.ignoredCount = 0
        self.dlCount = 0
        self.submodule = 0
        self.VER = "3.0"
        self.CHUNK = 2**15
        # signal.signal(signal.SIGTERM, self.graceExit)
        # signal.signal(signal.SIGINT, self.graceExit)

        sys.stdout.write('{}Natsume AI v{:s} {}{} {}\n\n'.format(self.CXMAGENTA, self.VER, self.CCYAN,"<Debugging Mode>" if debug else "", self.CRESET))

        self.argsParsed(self.utils.argsParser())
    
    def argsParsed(self, args: list):
        self.submodule = args.submodule
        if self.submodule == 'reddit':
            if (args.i): 
                self.redditParser.parser(args.subreddit, args.n, ignored=True)
            else: 
                self.redditParser.parser(args.subreddit, args.n)
        if self.submodule == 'nhentai':
            mode = 'info'
            if (args.rand): self.hentai.parser(None, 'random')
            if (args.dl): mode = 'download'
            if (args.s): mode = 'search-title'
            if (args.st): mode = 'search-tags'
            if (args.l): mode += '-showres'

            self.hentai.parser(args.sauce, mode)
        if self.submodule == 'imgur':
            self.imgurParser.parser(args.url, 'imgur')
        if self.submodule == 'ph':
            pass
        if self.submodule == 'auto':
            pass
        if self.submodule == 'anime':
            self.animeParser.parser(args.metaAnime, 'anime')
        if self.submodule == 'manga':
            self.animeParser.parser(args.metaManga, 'manga')
        if self.submodule == None:
            self.utils.printError("No Argument Given!!")
    
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