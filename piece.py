
from abc import ABC, abstractmethod
from ast import Match


BOARD_SIZE = 8 # Standard chess board size (8x8)

class Piece(ABC):
    """Abstract base class for all chess pieces."""

    def __init__(self, color: str):
        self.color = color  # 'white' or 'black'

    @abstractmethod
    def symbol(self) -> str:
        """
        Return a single-letter symbol for displaying on the board.
        Convention: uppercase for white, lowercase for black.
        """
        ...

    @abstractmethod
    def get_valid_moves(self, pos: tuple[int, int], board) -> list[tuple[int, int]]:
        """
        Calculate all legal moves for this piece from given position.
        - pos: Current (row, col) position
        - board: Board object to check positions
        Returns list of (row, col) target positions
        """
        ...

# ------------King Implementation------------------------------
class King(Piece):
    def symbol(self):
        return 'K' if self.color == 'white' else 'k' # White: K, Black: k

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos # Current row and column

        # Check all 8 surrounding squares
        for dr in (-1, 0, 1):     # Row offsets (-1, 0, +1)
            for dc in (-1, 0, 1): # Column offsets (-1, 0, +1)
                if dr == dc == 0: # Skip current position
                    continue

                nr, nc = r + dr, c + dc  # New position

                # Check if new position is on the board
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:

                    # Valid if empty or contains enemy piece
                    if board.is_empty((nr, nc)) or board.is_enemy((nr, nc), self.color):
                        moves.append((nr, nc))
        return moves


# ------------Queen Implementation------------------------------

class Queen(Piece):
    def symbol(self):
        return 'Q' if self.color == 'white' else 'q' # White: Q, Black: q

    def get_valid_moves(self, pos, board):
        # Queen moves like rook + bishop (all directions)
        return board.collect_line_moves(pos, self.color,
                                         directions=[
                                            (1,0),(-1,0),(0,1),(0,-1),(1,1), # Rook directions
                                            (-1,-1),(1,-1),(-1,1)]) # Bishop directions


class Rook(Piece):
    def symbol(self):
        return 'R' if self.color == 'white' else 'r' # White: R, Black: r

    def get_valid_moves(self, pos, board):

        # Rook moves in straight lines (horizontal/vertical)
        return board.collect_line_moves(pos, self.color, directions=[(1,0),(-1,0),(0,1),(0,-1)]) # Up, down, left, right


class Bishop(Piece):
    def symbol(self):
        return 'B' if self.color == 'white' else 'b' # White: B, Black: b

    def get_valid_moves(self, pos, board):

        # Bishop moves diagonally
        return board.collect_line_moves(pos, self.color, directions=[(1,1),(-1,-1),(1,-1),(-1,1)]# All four diagonals
)


class Knight(Piece):
    def symbol(self):
        return 'N' if self.color == 'white' else 'n' # White: N, Black: n

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos

        # All 8 possible L-shaped moves
        for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            nr, nc = r + dr, c + dc

            # Check if new position is on board
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:

                # Valid if empty or enemy
                if board.is_empty((nr, nc)) or board.is_enemy((nr, nc), self.color):
                    moves.append((nr, nc))
        return moves


class Pawn(Piece):
    def symbol(self):
        return 'P' if self.color == 'white' else 'p' # White: P, Black: p

    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos

        # Movement direction (white moves up, black moves down)
        direction = -1 if self.color == 'white' else 1

        # single step forward
        nr = r + direction
        if 0 <= nr < BOARD_SIZE and board.is_empty((nr, c)):
            moves.append((nr, c))
            # double step from start row
            start_row = 6 if self.color == 'white' else 1
            if r == start_row and board.is_empty((nr + direction, c)):
                moves.append((nr + direction, c))
        # Diagonal captures
        for dc in (-1, 1): # Left and right capture
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
