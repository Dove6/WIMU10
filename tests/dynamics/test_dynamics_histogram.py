import muspy as mp
from tests.dynamics.utils import create_sparse_array, create_track_going_up

from wimu10 import compute_dynamics_histogram


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == create_sparse_array(128, 0, [(100, 1)])


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == create_sparse_array(128, 0, [(100, 2)])


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == create_sparse_array(128, 0, [(100, 1), (101, 1)])


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == create_sparse_array(128, 0, [(100, 255)])


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == [0] + [1] * 127


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
    hist = compute_dynamics_histogram(piece, 0)
    assert hist == create_sparse_array(128, 0, [(velocities[0], 99), (velocities[1], 100), (velocities[2], 101)])
