from structure import extensions
import json, os

class NatsumePersonalityMan(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__VER = 1.0
        self.name = "personality"
        self.alias = [self.name, "persona"]
        self.desc = "Natsume's Personality Manager"
        self.args = [ 
            {
                "name": "mode",
                "desc": "Mode to Use"
            }
        ]
        self.isSystem = True
        self.personas = dict()
        self.currPersona = dict()
        self.personaDir = os.path.join("ext", "core", "personalities")
        self.init()

    def init(self):
        for persona in os.listdir(self.personaDir):
            with open(os.path.join(self.personaDir, persona), "r+") as f:
                self.personas[persona.split(".")[0]] = json.load(f)

        self.currPersona = self.personas[self.base.ExtLoader.settings["natsume"]["persona"]]

    def execute(self, mode):
        if mode in self.personas:
            self.base.settings["natsume"]["persona"] = mode
            
            print("Current Persona: {}".format(mode))
        else:
            self.utils.printError("Personality", f"{mode} is not a valid personality")