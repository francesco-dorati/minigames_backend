from games.tris import Tris


class Game:
    available_games = ['tris']

    def __init__(self, game_name):
        if game_name not in self.available_games:
            raise Exception('Game Unavailable')

        self.name = game_name

        if self.name == 'tris':
            self.max_players = 2
            self.status = 0     # 1 started 2 ended 0 normal
            self.game = Tris()

    def start(self):
        self.status = 1

    def play(self, move: str):
        pass
