class Tris:
    def __init__(self):
        self.max_players = 2
        self.turn = 0
        self.winner = None
        self.grid = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def play(self, pos: str) -> int:  # returns 0 if wrong, 1 if ok
        # position is "r c"
        r = int(pos[0])
        c = int(pos[1])

        if self.grid[r][c] != -1:
            return 0

        self.grid[r][c] = self.turn

        w = self.check_winner()
        if w in [0, 1, 2]:
            self.winner = w
        else:
            self.turn = (self.turn + 1) % 2

        return 1

    def check_winner(self) -> int:  # returns -1 if no winner, 2 if full, otherwise winner [1,2]
        full_flag = True
        col_flag = [-1, -1, -1]
        diag_flag = [-1, -1]

        for r, row in enumerate(self.grid):
            row_flag = -1
            for i, e in enumerate(row):
                # print(f"r: {r}, c: {i}, el: {e}, full: {full_flag}, row: {row_flag},col:{col_flag},diag: {diag_flag}")
                # full
                if e == 0:
                    full_flag = False

                # rows
                if i == 0:
                    row_flag = e
                elif e != row_flag:
                    row_flag = -1

                if i == 2 and row_flag != -1:
                    return row_flag

                # cols
                if r == 0:
                    col_flag[i] = e
                elif e != col_flag[i]:
                    col_flag[i] = -1

                if r == 2 and col_flag[i] != -1:
                    return col_flag[i]

                # diag
                if r == 0:
                    if i == 0:
                        diag_flag[0] = e
                    elif i == 2:
                        diag_flag[1] = e
                elif r == 1 and i == 1:
                    if e != diag_flag[0]:
                        diag_flag[0] = -1
                    if e != diag_flag[1]:
                        diag_flag[1] = -1
                elif r == 2:
                    if i == 0 and e == diag_flag[1]:
                        return diag_flag[1]
                    elif i == 2 and e == diag_flag[0]:
                        return diag_flag[0]

        return 2 if full_flag else -1

    def reset(self):
        self.turn = (self.turn + 1) % 2
        self.winner = None
        self.grid = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def json(self):
        return f"""
            turn: {self.turn},
            winner: {self.winner},
            grid: {self.grid}
        """
