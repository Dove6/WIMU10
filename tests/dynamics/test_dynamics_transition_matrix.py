import muspy as mp
from tests.dynamics.utils import create_sparse_matrix, create_track_going_up

from wimu10 import compute_dynamics_transition_matrix


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(128, 0, [])).all()


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(128, 0, [((100, 100), 1)])).all()


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(128, 0, [((100, 101), 1)])).all()


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(128, 0, [((100, 100), 254)])).all()


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (transition_matrix == create_sparse_matrix(128, 0, [((i + 1, i + 2), 1) for i in range(126)])).all()


def test_series_of_notes_of_three_velocities():
    velocities = [40, 80, 120]

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
    transition_matrix = compute_dynamics_transition_matrix(piece, 0)
    assert (
        transition_matrix
        == create_sparse_matrix(
            128,
            0,
            [
                ((velocities[0], velocities[0]), 65),
                ((velocities[0], velocities[1]), 33 + 1),
                ((velocities[1], velocities[1]), 66),
                ((velocities[1], velocities[2]), 33 + 1),
                ((velocities[2], velocities[0]), 32 + 1),
                ((velocities[2], velocities[2]), 66 + 1),
            ],
        )
    ).all()
