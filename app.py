# from flask import Flask, jsonify
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from user import User
from lobby import Lobby

# app = Flask(__name__)

# LOBBY TCP


# lobby kick <userid>
# lobby exit
# lobby info
# OK {
#   lobby_code: 123456,
#   game: tetris
#   players: [{id: <adminid>, color: 'blue'}, {id: <user>, color: 'red'}]
# }
#
# NOTIFICATIONS:
# {
#   massage/notification: 0'OK'
#   ...: {}
#   lobby: {}
# }
# JOINED {lobby}
# EXITED {lobby}
# lobby add bot easy

# game start
# game info
# STARTED {
#   id: 13123,
#   users: [<user>, <user>],
#   status: 0,
#
#   game: {
#       turn: 0,
#       winner: None, 0, 1
#       table: [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
#   }
#   turn: 1,
#
# }
# game play 11
# OK {
#   turn: 2,
#   table: [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
# }
# INVALID
# END {
#   winner: <userid>,
#   table: [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
# }

class App:
    def __init__(self):
        self.server = ('', 8080)
        self.active_lobbies = []

    def start(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(self.server)
        s.listen(5)
        print(f"Listening on port {self.server[1]}...")

        while True:
            conn, client = s.accept()

            print(f"{client[0]}:{client[1]} connected.")

            t = Thread(target=self.controller, args=(conn,))
            t.start()

    def controller(self, conn):
        user = None
        lobby = None

        def err():
            conn.send('ERR'.encode('utf-8'))

        while True:
            req = conn.recv(2048)
            if req == b'':
                conn.close()
                return

            req = req.decode('utf-8').split()

            # CREATE LOBBY
            # create <game> <userid>
            if req[0] == 'create':
                if not (req[1] and req[2]):
                    err()
                else:
                    game_name = req[1]
                    user_id = req[2]

                    if game_name in Lobby.available_games:
                        # create lobby
                        user = User(user_id, conn)
                        lobby = Lobby(user, game_name)
                        self.active_lobbies.append(lobby)

                        # respond
                        res = f"OK {lobby.json()}".encode('utf-8')
                        conn.send(res)
                    else:
                        err()

            # JOIN LOBBY
            # join <lobby_id> <user_id>
            elif req[0] == 'join':
                if not (req[1] and req[2]):
                    err()
                else:
                    lobby_id = int(req[1])
                    user_id = req[2]

                    user = User(user_id, conn)
                    lobby = self.get_lobby(lobby_id)
                    if not lobby:
                        conn.send("NULL".encode('utf-8'))
                    else:
                        ok = lobby.join(user)
                        if ok:
                            lobby.broadcast(f"JOINED {lobby.json()}")
                        else:
                            conn.send("FULL".encode('utf-8'))

            # LOBBY
            elif req[0] == 'lobby':
                if not (user and lobby):
                    err()
                else:
                    # lobby exit
                    if req[1] == 'exit':
                        lobby.exit(user)
                        if len(lobby.users) == 0:
                            # remove lobby
                            self.active_lobbies.remove(lobby)
                        else:
                            # notify the other users
                            lobby.broadcast(f"EXITED {lobby.json()}")

                        conn.send("CLOSING".encode('utf-8'))
                        conn.close()
                        return

                    # lobby kick <user_id>
                    elif req[1] == 'kick':
                        pass

            # GAME
            elif req[0] == 'game':
                if not (user and lobby) or not req[1]:
                    err()
                else:
                    # game start
                    if req[1] == 'start':
                        if lobby.is_admin(user):
                            lobby.status = 1
                            lobby.broadcast(f"STARTED {lobby.json()}")
                        else:
                            err()

                    # game play <move>
                    elif req[1] == 'play':
                        if not req[2]:
                            err()
                        elif lobby.status == 1 and user.id == lobby.users[lobby.game.turn].id:
                            r = lobby.game.play(req[2])
                            if r != 0:
                                err()
                            elif lobby.game.winner in [0, 1, 2]:
                                lobby.status = 2
                                lobby.broadcast(f"END {lobby.json()}")
                            else:
                                lobby.broadcast(f"MOVE {lobby.json()}")
                        else:
                            err()

                    elif req[1] == 'reset':
                        if lobby.is_admin(user):
                            lobby.game.reset()
                            lobby.status = 0
                            lobby.broadcast(f"RESET {lobby.json()}")
                        else:
                            err()

                    elif req[1] == 'exit':
                        pass

            else:
                err()

    def get_lobby(self, lobby_id):
        for lobby in self.active_lobbies:
            if lobby.id == lobby_id:
                return lobby
        return None


if __name__ == "__main__":
    app = App()
    app.start()
