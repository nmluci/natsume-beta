from . import utils
import json
import os

class BaseModule():
    def __init__(self):
        self.utils = utils.NatsumeUtils()
        self.CRED = self.utils.CRED
        self.CCYAN = self.utils.CCYAN
        self.CXMAGENTA = self.utils.CXMAGENTA
        self.CMAGENTA = self.utils.CMAGENTA
        self.CRESET = self.utils.CRESET

        if os.path.isfile("config.fyn"):
            with open("config.fyn") as f:
                data = json.load(f)
                self.reddit = list()
                self.imgur = list()
                self.reddit.append(data['Reddit']["clientID"])
                self.reddit.append(data['Reddit']["clientSecret"])
                self.reddit.append(data['Reddit']["username"])
                self.reddit.append(data['Reddit']["password"])
                self.imgur.append(data['Imgur']['clientID'])
        else:
            print("{}NO CONFIG FOUND!!!{}".format(self.CXMAGENTA, self.CRESET))
            exit()
    