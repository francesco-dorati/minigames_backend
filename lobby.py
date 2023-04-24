import random

from user import User
from games.tris import Tris

# DATABASE = 'data/lobby'


class Lobby:
    available_games = ['tris']

    def __init__(self, user: User, game_name: str):
        self.id: str = random.randint(0, 999999)
        self.status = 0
        self.users: User = [user]

        if game_name == 'tris':
            self.game = Tris()

    def join(self, user: User) -> bool:
        if len(self.users) >= self.game.max_players:
            return False
        else:
            self.users.append(user)
            return True

    def exit(self, user):
        self.users.remove(user)

    def broadcast(self, s: str):
        for u in self.users:
            u.connection.send(s.encode('utf-8'))

    def is_admin(self, user: User):
        return self.users[0].id == user.id

    def json(self):
        return f"""
        id: {self.id}
        users: {[(u.json() if u else u) for u in self.users]}
        status: {self.status}
        game: {{ {self.game.json()} }}
        """


# def database():
#    connection = sqlite3.connect(DATABASE, check_same_thread=False)
#    c = connection.cursor()
#    c.execute("""CREATE TABLE IF NOT EXISTS Lobby (
#      id CHAR(6) PRIMARY KEY NOT NULL,
#      admin CHAR(6),
#      user CHAR(6) DEFAULT NULL,
#      game CHAR(6)
#    )""")
#    return c

