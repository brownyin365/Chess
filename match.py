from board import Board
from player import Player


class Match:
    def __init__(self):
        """Initialize a new chess match with board and players."""
        # Create a new chess board with pieces in starting positions
        self.board = Board()

        # Create two players (white and black)
        self.players = [Player('white'), Player('black')]

        # Start with white's turn (index 0)
        self.turn_index = 0

    @property
    def current_player(self):

        """Returns the player whose turn it is currently."""
        return self.players[self.turn_index]

    def switch_turn(self):
        """Alternate turns between white and black players."""
        # Toggles between 0 and 1:
        # 0 → 1 (white → black)
        # 1 → 0 (black → white)
        self.turn_index = 1 - self.turn_index

    def play_turn(self, start, end):
        """
        Attempt to make a move from start to end coordinates.
        Returns True if move was successful, False otherwise.
        
        Args:
            start: Tuple (row, col) of starting position
            end: Tuple (row, col) of target position
        """
        # Get piece at starting position
        piece = self.board.grid[start[0]][start[1]]

        # Check if:
        # 1. There is actually a piece at start position
        # 2. The piece belongs to current player
        if piece is None or piece.color != self.current_player.color:
            print("It's not your piece!")
            return False

        # Attempt to move the piece through board logic
        moved = self.board.move_piece(start, end)

        # If move was successful, switch turns
        if moved:
            self.switch_turn()
        return moved
