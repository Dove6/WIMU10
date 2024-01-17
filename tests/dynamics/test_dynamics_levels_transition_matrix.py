import muspy as mp
from tests.dynamics.utils import create_sparse_matrix, create_track_going_up

from wimu10 import compute_dynamics_levels_transition_matrix


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [])).all()


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [((5, 5), 1)])).all()


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [((5, 5), 1)])).all()


def test_two_notes_of_different_velocity_levels():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 95 + i)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [((4, 5), 1)])).all()


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [((5, 5), 254)])).all()


def test_series_of_notes_of_the_same_velocity_level():
    piece = mp.Music(
        tracks=[create_track_going_up(16, (0, 127), volume_func=lambda i: 96 + i)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(8, 0, [((5, 5), 15)])).all()


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (
        transition_matrix
        == create_sparse_matrix(
            8,
            0,
            [
                ((0, 0), 16),
                ((0, 1), 1),
                ((1, 1), 15),
                ((1, 2), 1),
                ((2, 2), 14),
                ((2, 3), 1),
                ((3, 3), 15),
                ((3, 4), 1),
                ((4, 4), 15),
                ((4, 5), 1),
                ((5, 5), 15),
                ((5, 6), 1),
                ((6, 6), 14),
                ((6, 7), 1),
            ],
        )
    ).all()


def test_series_of_notes_of_different_velocity_level_each():
    velocities = [20, 40, 60, 70, 80, 100, 120, 127]

    piece = mp.Music(
        tracks=[create_track_going_up(8, (0, 0), volume_func=lambda i: velocities[i])],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (
        transition_matrix
        == create_sparse_matrix(
            8,
            0,
            [
                ((0, 1), 1),
                ((1, 2), 1),
                ((2, 3), 1),
                ((3, 4), 1),
                ((4, 5), 1),
                ((5, 6), 1),
                ((6, 7), 1),
            ],
        )
    ).all()


def test_series_of_notes_of_three_velocity_levels():
    velocities = [40, 90, 120]

    def _volume_func(index: int) -> int:
        if index < 99:
            return velocities[index % 3]
        elif index == 99:
            return velocities[2]
        else:
            return velocities[(index - 99) // 67]

    piece = mp.Music(
        tracks=[create_track_going_up(300, (0, 127), volume_func=_volume_func)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_levels_transition_matrix(piece, 0)
    assert (
        transition_matrix
        == create_sparse_matrix(
            8,
            0,
            [
                ((1, 1), 65),
                ((1, 4), 33 + 1),
                ((4, 4), 66),
                ((4, 6), 33 + 1),
                ((6, 1), 32 + 1),
                ((6, 6), 66 + 1),
            ],
        )
    ).all()
