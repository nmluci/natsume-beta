import discord
from structure import extensions

class NatsumeDiscordAPI(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "discordman"
        self.isSystem = True
        self.alias = [self.name]

    def execute(self):
        return super().execute(None)