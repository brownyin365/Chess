
from abc import ABC, abstractmethod
from ast import Match


BOARD_SIZE = 8

class Piece(ABC):
    """Abstract base class for all chess pieces."""

    def __init__(self, color: str):
        self.color = color  # 'white' or 'black'

    @abstractmethod
    def symbol(self) -> str:
        """Return a single‑letter symbol for displaying on the board."""
        ...

    @abstractmethod
    def get_valid_moves(self, pos: tuple[int, int], board) -> list[tuple[int, int]]:
        """Return a list of legal target squares for the piece from the given position."""
        ...


class King(Piece):
    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board.is_empty((nr, nc)) or board.is_enemy((nr, nc), self.color):
                        moves.append((nr, nc))
        return moves


class Queen(Piece):
    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def get_valid_moves(self, pos, board):
        return board.collect_line_moves(pos, self.color,
                                         directions=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)])


class Rook(Piece):
    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def get_valid_moves(self, pos, board):
        return board.collect_line_moves(pos, self.color, directions=[(1,0),(-1,0),(0,1),(0,-1)])


class Bishop(Piece):
    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def get_valid_moves(self, pos, board):
        return board.collect_line_moves(pos, self.color, directions=[(1,1),(-1,-1),(1,-1),(-1,1)])


class Knight(Piece):
    def symbol(self):
        return 'N' if self.color == 'white' else 'n'

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos
        for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                if board.is_empty((nr, nc)) or board.is_enemy((nr, nc), self.color):
                    moves.append((nr, nc))
        return moves


class Pawn(Piece):
    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos
        direction = -1 if self.color == 'white' else 1
        # single step
        nr = r + direction
        if 0 <= nr < BOARD_SIZE and board.is_empty((nr, c)):
            moves.append((nr, c))
            # double step from start row
            start_row = 6 if self.color == 'white' else 1
            if r == start_row and board.is_empty((nr + direction, c)):
                moves.append((nr + direction, c))
        # captures
        for dc in (-1, 1):
            nc = c + dc
            if 0 <= nc < BOARD_SIZE:
                if board.is_enemy((nr, nc), self.color):
                    moves.append((nr, nc))
        return moves
    
    
def demo():
    """Simple CLI play demo (moves are hard‑coded for brevity)."""
    match = Match()
    print("Initial board:")
    print(match.board)
    # a couple of sample moves
    moves = [((6,4),(4,4)),  # white pawn e2‑e4
             ((1,4),(3,4)),  # black pawn e7‑e5
             ((7,6),(5,5)),  # white knight g1‑f3
             ((0,1),(2,2))]  # black knight b8‑c6
    for s, e in moves:
        print(f"\n{match.current_player.color} moves {s} -> {e}")
        match.play_turn(s, e)
        print(match.board)

if __name__ == "__main__":
    demo()