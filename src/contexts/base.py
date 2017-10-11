class Context:
    def __init__(self, drawer):
        self.drawer = drawer

    def execute(self):
        raise NotImplementedError
