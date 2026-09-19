class Joint:
    def __init__(self, name, limit=1.57):
        self.name, self.limit = name, limit
        self.rotation = [0.0, 0.0, 0.0]
    def reset(self): self.rotation[:] = [0.0, 0.0, 0.0]
