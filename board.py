from piece import BOARD_SIZE, Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self):
        # Initialize an 8x8 grid (BOARD_SIZE is presumably 8)
        # Each cell can contain either a Piece object or None (empty square)
        self.grid: list[list[Piece|None]] = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Set up initial chess position
        self._place_starting_pieces()


    # --- Helpers Methods -------------------------------------------------------------

    def is_empty(self, pos):
        """Check if a position is empty (no piece)."""
        r, c = pos # Unpack row and column
        return self.grid[r][c] is None

    def is_enemy(self, pos, color):
        """Check if a position contains an enemy piece of the given color."""
        r, c = pos
        piece = self.grid[r][c]
        # Returns True if there's a piece AND it's not the same color
        return piece is not None and piece.color != color

    def collect_line_moves(self, pos, color, directions):
        """
        Generate sliding moves (for bishops, rooks, queens).
        - pos: Current position (row, col)
        - color: Current player's color
        - directions: List of (dr, dc) direction vectors
        """
        moves = []
        for dr, dc in directions: # For each direction (e.g., (1,0) for down)
            r, c = pos
            while True:
                r += dr # Move in direction
                c += dc
                # Check if still on board
                if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                    break
                if self.is_empty((r, c)):
                    moves.append((r, c)) # Valid empty square
                elif self.is_enemy((r, c), color):
                    moves.append((r, c)) # Can capture enemy
                    break # Can't move past enemy
                else:
                    break # Friendly piece blocks
        return moves

    # --------------Board Setup----------------------------------------------------------

    def _place_starting_pieces(self):
        """Set up standard chess starting position."""
        # Pawns (row 1 for black, row 6 for white)
        for c in range(BOARD_SIZE):
            self.grid[1][c] = Pawn('black')
            self.grid[6][c] = Pawn('white')

        # other pieces order: R N B Q K B N R
        # Back row pieces in standard order
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c, piece_cls in enumerate(placement):
            self.grid[0][c] = piece_cls('black') # Black back row
            self.grid[7][c] = piece_cls('white') # White back row

    def move_piece(self, start: tuple[int,int], end: tuple[int,int]) -> bool:
        """
        Attempt to move a piece from start to end.
        Returns True if move is legal and executed.
        """
        sr, sc = start # Unpack start position
        er, ec = end  # Unpack end position
        piece = self.grid[sr][sc]
        if piece is None:
            print("No piece at start square")
            return False # Can't move empty square

        # Check if move is in piece's valid moves
        if end not in piece.get_valid_moves(start, self):
            print("Illegal move for", piece.__class__.__name__)
            return False
        # Execute move
        self.grid[er][ec] = piece  # Place piece at destination
        self.grid[sr][sc] = None   # Clear original position
        return True

    def __str__(self):
        """String representation of the board for debugging."""

        rows = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                piece = self.grid[r][c]
                # Use piece symbol if exists, '.' for empty
                row.append(piece.symbol() if piece else '.')
            rows.append(' '.join(row))  # Join row with spaces
        return '\n'.join(rows)  # Join rows with newlines
