from board import Board
from player import Player


class Match:
    def __init__(self):
        self.board = Board()
        self.players = [Player('white'), Player('black')]
        self.turn_index = 0

    @property
    def current_player(self):
        return self.players[self.turn_index]

    def switch_turn(self):
        self.turn_index = 1 - self.turn_index

    def play_turn(self, start, end):
        piece = self.board.grid[start[0]][start[1]]
        if piece is None or piece.color != self.current_player.color:
            print("It's not your piece!")
            return False
        moved = self.board.move_piece(start, end)
        if moved:
            self.switch_turn()
        return moved
