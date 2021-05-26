import discord
from structure import extensions

class NatsumeDiscordAPI(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "discordman"
        self.isSystem = True

    def execute(self, args):
        return super().execute(args)