from structure import extensions
import json, os

class NatsumePersonalityMan(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.__VER = 1.0
        self.name = "personality"
        self.desc = "Natsume's Personality Manager"
        self.args = {
            "opt": "Mode to Use"
        }
        self.isSystem = True
        self.personas = dict()
        self.currPersona = dict()
        self.personaDir = os.path.join("ext", "admin", "personalities")
        self.init()

    def init(self):
        for persona in os.listdir(self.personaDir):
            with open(os.path.join(self.personaDir, persona), "r+") as f:
                self.personas[persona.split(".")[0]] = json.load(f)

        self.currPersona = self.personas[self.base.settings["natsume"]["persona"]]

    def execute(self, args):
        if args and args[0] in self.personas:
            self.currPersona = self.personas[args[0]]
            print("Current Persona: {}".format(args))