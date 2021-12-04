from structure import extensions

class NatsumeSettings(extensions.NatsumeExt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "setting"
        self.isSystem = True
        self.alias = [self.name]

    def execute(self, args):
        for subset in self.base.settings:
            print(subset, self.base.settings[subset])