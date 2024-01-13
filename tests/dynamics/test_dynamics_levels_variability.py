import muspy as mp
import numpy as np
import pytest
from tests.dynamics.utils import create_track_going_up

from wimu10 import compute_dynamics_levels_variability


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [0]
    assert variability.total_count == 0
    assert np.isclose(variability.ratio, [0.0]).all()


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [0]
    assert variability.total_count == 1
    assert np.isclose(variability.ratio, [0.0]).all()


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [0]
    assert variability.total_count == 1
    assert np.isclose(variability.ratio, [0.0]).all()


def test_two_notes_of_different_velocity_levels():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 95 + i)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [1]
    assert variability.total_count == 1
    assert np.isclose(variability.ratio, [1.0]).all()


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [0]
    assert variability.total_count == 254
    assert np.isclose(variability.ratio, [0.0]).all()


def test_series_of_notes_of_the_same_velocity_level():
    piece = mp.Music(
        tracks=[create_track_going_up(16, (0, 127), volume_func=lambda i: 96 + i)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [0]
    assert variability.total_count == 15
    assert np.isclose(variability.ratio, [0.0]).all()


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [7]
    assert variability.total_count == 126
    assert np.isclose(variability.ratio, [7 / 126]).all()


def test_series_of_notes_of_different_velocity_level_each():
    velocities = [20, 40, 60, 70, 80, 100, 120, 127]

    piece = mp.Music(
        tracks=[create_track_going_up(8, (0, 0), volume_func=lambda i: velocities[i])],
        resolution=16,
    )
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1])
    assert variability.changes_count == [7]
    assert variability.total_count == 7
    assert np.isclose(variability.ratio, [1.0]).all()


@pytest.mark.parametrize('difference_level', [1, 2])
def test_series_of_notes_of_three_velocity_levels(difference_level: int):
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
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[difference_level])
    assert variability.changes_count == [101]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [101 / 299]).all()


@pytest.mark.parametrize('difference_level', [4, 5])
def test_series_of_notes_of_three_velocity_levels_with_greater_difference_level(difference_level: int):
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
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[difference_level])
    assert variability.changes_count == [33]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [33 / 299]).all()


def test_series_of_notes_of_three_velocity_levels_with_too_great_difference_level():
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
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[6])
    assert variability.changes_count == [0]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [0 / 299]).all()


def test_series_of_notes_of_three_velocities_with_two_difference_levels():
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
    variability = compute_dynamics_levels_variability(piece, 0, difference_levels=[1, 4])
    assert variability.changes_count == [68, 33]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [68 / 299, 33 / 299]).all()
