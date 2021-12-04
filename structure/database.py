from pathlib import Path

from . import utils

class NatsumeDatabase:
    def __init__(self):
        self.utils = utils.NatsumeUtils()
        self.config = self.utils.getConfig()["database"]
        