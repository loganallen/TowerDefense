class Path3():
    def __init__(self):
        self.path = []

        self.path.append((10,130))
        self.path.append((85,130))

        self.path.append((85,605))
        self.path.append((641,605))
        self.path.append((641,250))
        self.path.append((350,250))
        self.path.append((350,375))
        self.path.append((495,375))
        self.path.append((495,495))
        self.path.append((210,495))
        self.path.append((210,130))
        self.path.append((775,130))
        self.path.append((775,610))

        self.path.append((835,608))

    def getPath(self):
        return self.path