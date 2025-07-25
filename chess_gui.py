import tkinter as tk
from tkinter import messagebox
from match import Match

SQUARE = 80
PIECE_FONT = ('Arial', 24, 'bold')
UNICODE_MAP = {
    'K': '\u2654', 'Q': '\u2655', 'R': '\u2656',
    'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
    'k': '\u265A', 'q': '\u265B', 'r': '\u265C',
    'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
}

class ChessGUI:
    def __init__(self, root):
        self.match = Match()
        self.root = root
        self.root.title("Python Chess")
        self.canvas = tk.Canvas(root, width=8*SQUARE, height=8*SQUARE)
        self.canvas.pack()
        self.selected = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                x1 = c * SQUARE
                y1 = r * SQUARE
                color = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x1 + SQUARE, y1 + SQUARE, fill=color, outline="")
                piece = self.match.board.grid[r][c]
                if piece:
                    symbol = UNICODE_MAP.get(piece.symbol(), '?')
                    self.canvas.create_text(x1 + SQUARE//2, y1 + SQUARE//2, text=symbol, font=PIECE_FONT)
        if self.selected:
            r, c = self.selected
            self.canvas.create_rectangle(c*SQUARE, r*SQUARE, c*SQUARE+SQUARE, r*SQUARE+SQUARE, outline="red", width=3)

    def on_click(self, event):
        col = event.x // SQUARE
        row = event.y // SQUARE
        if self.selected:
            moved = self.match.play_turn(self.selected, (row, col))
            self.selected = None
            self.draw_board()
            if moved and hasattr(self.match, 'finished') and self.match.finished:
                winner = self.match.current_player.color
                messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            piece = self.match.board.grid[row][col]
            if piece and piece.color == self.match.current_player.color:
                self.selected = (row, col)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
