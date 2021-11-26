#!/usr/bin/env python
from random import shuffle
from pprint import pprint
from typing import Tuple, Union, List, Sequence, Iterator
from collections import defaultdict

# sides
PB = 'pink-base'
PT = 'pink-top'
BB = 'blue-base'
BT = 'blue-top'
WT = 'brown-top'
WB = 'brown-base'
YT = 'yellow-top'
YB = 'yellow-base'

Side = str
Piece = Tuple[Side, Side, Side, Side]

opposing_sides = { PB: PT, WB: WT, YB: YT, BB: BT }
for side, opposing_side in dict(opposing_sides).items():
    opposing_sides[opposing_side] = side


pieces: Tuple[Piece, ...] = (
    (BT, BB, YB, WB),
    (WT, YB, BT, PT),
    (PB, BB, WT, YT),
    (WB, YB, PT, BT),
    (PT, WT, YT, BT),
    (YT, PT, WT, WT),
    (PT, WB, YB, BT),
    (YT, WT, PB, BT),
    (PB, BB, YT, WB),
)


# We choose to represent the board as an order starting with the
# center piece, then clockwise from the center left piece.

# a piece at this 0-indexed spot needs to match up with the piece(s)
# at the given 0-indexed spots.
raw_board_spot_edges = (
    # each inner tuple is indexed by edge - L, U, R, D
    (1, 3, 5, 7),
    (None, 2, 0, 8),
    (None, None, 3, 1),
    (2, None, 4, 0),
    (3, None, None, 5),
    (0, 4, None, 6),
    (7, 5, None, None),
    (8, 0, 6, None),
    (None, 1, 7, None)
)


board_spot_edges = list()
for i, spot_edges in enumerate(raw_board_spot_edges):
    needed_spot_edges = list()
    for spot_edge in spot_edges:
        if spot_edge is None or spot_edge < i:
            needed_spot_edges.append(spot_edge)
        else:
            needed_spot_edges.append(None)  # won't be ready for comparison yet
    board_spot_edges.append(tuple(needed_spot_edges))


L = 0
U = 1
R = 2
D = 3
pdirs = ('L', 'U', 'R', 'D')


Direction_of_matching_edge = (
    # the index of board_spot_edges is also used to index into this
    (None, None, None, None),
    (None, None, L, None),
    (None, None, None, U),
    (R, None, None, U),
    (R,),
    (R, D),
    (None, D),
    (None, D, L),
    (None, D, L),
)


def piece_rotations(piece: Piece) -> Iterator[Piece]:
    yield piece
    yield tuple([piece[1], piece[2], piece[3], piece[0]])
    yield tuple([piece[2], piece[3], piece[0], piece[1]])
    yield tuple([piece[3], piece[0], piece[1], piece[2]])


def pspotedge(direction, spot):
    return pdirs[direction], spot


def rot_piece_matches(board: Sequence[Piece], rot_piece: Piece) -> bool:
    needed_spots = board_spot_edges[len(board)]
    for direction_on_rot_piece, needed_spot in enumerate(needed_spots):
        if needed_spot is None:
            continue  # no need to match an empty side
        direction_of_matching_edge = Direction_of_matching_edge[len(board)][direction_on_rot_piece]
        placed_piece = board[needed_spot]
        if placed_piece[direction_of_matching_edge] != opposing_sides[rot_piece[direction_on_rot_piece]]:
            return False
    return True


spot_att = defaultdict(int)
spot_matches = defaultdict(int)


def fill_board(board, rem_pieces, emit_solution):
    global spot_att, spot_matches
    assert len(board) + len(rem_pieces) == 9
    for i, piece in enumerate(rem_pieces):
        for piece_rotation in piece_rotations(piece):
            spot_att[len(board)] += 1
            if rot_piece_matches(board, piece_rotation):
                spot_matches[len(board)] += 1
                new_rem_pieces = rem_pieces[:i] + rem_pieces[i + 1:]
                assert piece not in new_rem_pieces
                out_board = fill_board(board + [piece_rotation], new_rem_pieces, emit_solution)
                if len(out_board) == 9:
                    emit_solution(out_board)
                    break
    return board


def run():
    global spot_att, spot_matches
    solutions = list()
    def emit_solution(board):
        solutions.append(board)
    for center_piece in pieces:
        print('CENTER:', center_piece)
        rem_pieces = [ piece for piece in pieces if piece is not center_piece ]
        assert len(rem_pieces) == 8
        board = fill_board([center_piece], rem_pieces, emit_solution)
        pprint(spot_att)
        pprint(spot_matches)
    return solutions


def test_board_spot_edges():
    spot_links = defaultdict(int)
    for spot in raw_board_spot_edges:
        for edge in spot:
            spot_links[edge] += 1
    assert spot_links[None] == 12
    assert spot_links[0] == 4
    assert spot_links[2] == 2
    assert spot_links[4] == 2
    assert spot_links[6] == 2
    assert spot_links[8] == 2
    assert spot_links[1] == 3
    assert spot_links[3] == 3
    assert spot_links[5] == 3
    assert spot_links[7] == 3


test_board_spot_edges()


def test_rot_piece_matches():
    print('testing\n\n')
    assert rot_piece_matches(pieces[:3], pieces[3])
    assert rot_piece_matches(pieces[:2], pieces[2])
    assert not rot_piece_matches(pieces[:1], pieces[1])

test_rot_piece_matches()


pprint(run())
