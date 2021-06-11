from structure import extensions

class NatsumeSettings(extensions.NatsumeExt):
    def __init__(self, main):
        super().__init__(main)
        self.name = "setting"
        self.isSystem = True

    def execute(self, args):
        for subset in self.base.settings:
            print(subset, self.base.settings[subset])