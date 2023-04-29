import random


class User:
    def __init__(self, name: str, conn):
        # get data from id
        self.id: int = random.randint(0, 999999)
        self.name = name
        self.connection = conn
        self.color = None

    def json(self):
        return f"""|{self.id} - {self.name}|"""

