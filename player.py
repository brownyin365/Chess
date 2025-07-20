class Player:
    def __init__(self, color: str):
        self.color = color  # 'white' or 'black'

    def __repr__(self):
        return f"Player({self.color})"