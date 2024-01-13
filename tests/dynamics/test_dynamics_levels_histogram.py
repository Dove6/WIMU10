import muspy as mp
from tests.dynamics.utils import create_sparse_array, create_track_going_up

from wimu10 import compute_dynamics_levels_histogram


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(5, 1)])


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(5, 2)])


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(5, 2)])


def test_two_notes_of_different_velocity_level():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 95 + i)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(4, 1), (5, 1)])


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(5, 255)])


def test_series_of_notes_of_the_same_velocity_level():
    piece = mp.Music(
        tracks=[create_track_going_up(16, (0, 127), volume_func=lambda i: 96 + i)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == create_sparse_array(8, 0, [(5, 16)])


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == [17, 16, 15, 16, 16, 16, 15, 1]


def test_series_of_notes_of_different_velocity_level_each():
    velocities = [20, 40, 60, 70, 80, 100, 120, 127]

    piece = mp.Music(
        tracks=[create_track_going_up(8, (0, 0), volume_func=lambda i: velocities[i])],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == [1] * 8


def test_series_of_notes_of_three_velocity_levels():
    velocities = [40, 90, 120]

    def _volume_func(index: int) -> int:
        if index < 99:
            return velocities[index % 3] + (index % 3 - 1)
        elif index == 99:
            return velocities[2] + (index % 3 - 1)
        else:
            return velocities[(index - 99) // 67] + (index % 3 - 1)

    piece = mp.Music(
        tracks=[create_track_going_up(300, (0, 127), volume_func=_volume_func)],
        resolution=16,
    )
    hist = compute_dynamics_levels_histogram(piece, 0)
    assert hist == [0, 99, 0, 0, 100, 0, 101, 0]
