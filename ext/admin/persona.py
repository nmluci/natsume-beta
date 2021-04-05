from structure import extensions
import json, os

class NatsumePersonalityMan(extensions.NatsumeExt):
    def __init__(self):
        super().__init__()
        self.__VER = 1.0
        self.name = "personality"
        self.desc = "Natsume's Personality Manager"
        self.args = {
            "opt": "Mode to Use"
        }
        self.isSystem = True
        self.personas = dict()

    def execute(self, main, args = []):
        self.init()

    def init(self):
        print(os.listdir())