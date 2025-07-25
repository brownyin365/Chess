class Player:
    def __init__(self, color: str, name: str = None, rating: int = 0):
        self.color = color
        self.name = name or f"Player_{color}"  # Default name if none provided
        self.rating = rating
        self.captured_pieces = []  # Track pieces captured by this player
        self.move_history = []     # Record all moves made
        
    def add_captured_piece(self, piece):
        """Record when this player captures an opponent's piece"""
        self.captured_pieces.append(piece)
        
    def record_move(self, move):
        """Add a move to this player's history"""
        self.move_history.append(move)
        
    def __repr__(self):
        return (f"Player(color={self.color!r}, "
                f"name={self.name!r}, "
                f"rating={self.rating})")
