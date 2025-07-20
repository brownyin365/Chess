from piece import BOARD_SIZE, Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self):
        self.grid: list[list[Piece|None]] = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._place_starting_pieces()

    # --- Helpers -------------------------------------------------------------

    def is_empty(self, pos):
        r, c = pos
        return self.grid[r][c] is None

    def is_enemy(self, pos, color):
        r, c = pos
        piece = self.grid[r][c]
        return piece is not None and piece.color != color

    def collect_line_moves(self, pos, color, directions):
        """Utility for sliding pieces."""
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                    break
                if self.is_empty((r, c)):
                    moves.append((r, c))
                elif self.is_enemy((r, c), color):
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

    # ------------------------------------------------------------------------

    def _place_starting_pieces(self):
        """Standard chess starting position."""
        # pawns
        for c in range(BOARD_SIZE):
            self.grid[1][c] = Pawn('black')
            self.grid[6][c] = Pawn('white')
        # other pieces order: R N B Q K B N R
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c, piece_cls in enumerate(placement):
            self.grid[0][c] = piece_cls('black')
            self.grid[7][c] = piece_cls('white')

    def move_piece(self, start: tuple[int,int], end: tuple[int,int]) -> bool:
        """Attempt to move a piece; return True if legal and executed."""
        sr, sc = start
        er, ec = end
        piece = self.grid[sr][sc]
        if piece is None:
            print("No piece at start square")
            return False
        if end not in piece.get_valid_moves(start, self):
            print("Illegal move for", piece.__class__.__name__)
            return False
        # Execute move
        self.grid[er][ec] = piece
        self.grid[sr][sc] = None
        return True

    def __str__(self):
        rows = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                piece = self.grid[r][c]
                row.append(piece.symbol() if piece else '.')
            rows.append(' '.join(row))
        return '\n'.join(rows)
