
from ast import Match
import sys
from match import Match


def parse_square(sq: str) -> tuple[int, int]:
    files = 'abcdefgh'
    try:
        file = files.index(sq[0].lower())
        rank = 8 - int(sq[1])
        return rank, file
    except (ValueError, IndexError):
        raise ValueError(f"Invalid square notation: {sq}")

def main():
    match = Match()
    print("\nWelcome to CLI Chess! Enter moves in algebraic coordinate form, e.g., 'e2 e4'. Type 'quit' to exit.\n")
    while True:
        print(match.board)
        player = match.current_player.color
        move_input = input(f"\n{player} to move > ").strip()
        if move_input.lower() in {'quit', 'exit'}:
            print("Goodbye!")
            break
        parts = move_input.split()
        if len(parts) != 2:
            print("Please enter a move as: <from> <to>  e.g.,  e2 e4")
            continue
        try:
            start = parse_square(parts[0])
            end = parse_square(parts[1])
        except ValueError as e:
            print(e)
            continue
        if not match.play_turn(start, end):
            print("Move failed – try again.")
            continue

if __name__ == "__main__":
    main()
