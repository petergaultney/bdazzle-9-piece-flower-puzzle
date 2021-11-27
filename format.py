"""ASCII formatting for square board pieces"""
WIDTH = 20


def format_piece(piece) -> list:
    l, t, r, b  = piece
    t = t.replace('-', ' ')
    b = b.replace('-', ' ')
    lt, lb = l.split('-')
    rt, rb = r.split('-')
    sb = lambda s: "|" + s + "|"

    return (
        f"┌" + "-" * WIDTH + "+",
        sb(t.center(WIDTH)),
        sb(" " * WIDTH),
        sb(" " * WIDTH),
        sb(f" {lt:<9}{rt:>9} "),
        sb(f" {lb:<9}{rb:>9} "),
        sb(" " * WIDTH),
        sb(" " * WIDTH),
        sb(b.center(WIDTH)),
        "+" + "-" * WIDTH + "┘",
    )


def reorder_board(board):
    """Left to right cols, and top-down rows"""
    board_order = [2, 3, 4, 1, 0, 5, 8, 7, 6]
    return [board[i] for i in board_order]


def matrix_board(H, W, raw_board):
    board = reorder_board(raw_board)
    rows = list()
    for r in range(H):
        row = list()
        for c in range(W):
            row.append(board[r*W+c])
        rows.append(row)
    return rows


def format_row(row):
    lines = list()
    for piece in row:
        if not lines:
            lines = format_piece(piece)
        else:
            lines = [existing_line + new_line for existing_line, new_line in zip(lines, format_piece(piece))]
    return lines



def colorize(lines):
    reset = "\033[0m"
    try:
        text_onto_colors = dict(
            yellow='\033[38;5;190m',
            brown='\033[38;5;94m',
            blue='\033[38;5;63m',
            pink='\033[38;5;175m',
            top='\033[48;5;15m',
            base='\033[48;5;0m',
        )

        for line in lines:
            for text, color in text_onto_colors.items():
                line = line.replace(text, color + text + reset)
            yield line
    except:
        yield from lines


def format_board(board, H = 3, W = 3) -> str:
    lines = list()
    for row in matrix_board(H, W, board):
        lines += format_row(row)
    return '\n'.join(colorize(lines))
