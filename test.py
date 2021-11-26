from collections import defaultdict

from solve import raw_board_spot_edges, rot_piece_matches, pieces


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
    assert rot_piece_matches(pieces[:3], pieces[3])
    assert rot_piece_matches(pieces[:2], pieces[2])
    assert not rot_piece_matches(pieces[:1], pieces[1])


test_rot_piece_matches()
