class User:
    def __init__(self, id: int, conn):
        # get data from id
        self.id: int = id
        self.connection = conn
        self.color = None

    def json(self):
        return f"""id: {self.id}"""

