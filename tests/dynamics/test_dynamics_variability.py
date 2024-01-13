import muspy as mp
import numpy as np
import pytest
from tests.dynamics.utils import create_track_going_up

from wimu10 import compute_dynamics_variability


def test_single_note():
    piece = mp.Music(
        tracks=[create_track_going_up(1, (0, 0), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_variability(piece, 0)
    assert variability.changes_count == [0]
    assert variability.total_count == 0
    assert np.isclose(variability.ratio, [0.0]).all()


def test_two_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_variability(piece, 0)
    assert variability.changes_count == [0]
    assert variability.total_count == 1
    assert np.isclose(variability.ratio, [0.0]).all()


def test_two_notes_of_different_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(2, (0, 0), volume_func=lambda i: 100 + i)],
        resolution=16,
    )
    variability = compute_dynamics_variability(piece, 0)
    assert variability.changes_count == [1]
    assert variability.total_count == 1
    assert np.isclose(variability.ratio, [1.0]).all()


def test_series_of_notes_of_the_same_velocity():
    piece = mp.Music(
        tracks=[create_track_going_up(255, (0, 127), volume_func=100)],
        resolution=16,
    )
    variability = compute_dynamics_variability(piece, 0)
    assert variability.changes_count == [0]
    assert variability.total_count == 254
    assert np.isclose(variability.ratio, [0.0]).all()


def test_series_of_notes_of_different_velocity_each():
    piece = mp.Music(
        tracks=[create_track_going_up(127, (0, 0), volume_func=lambda i: i + 1)],
        resolution=16,
    )
    variability = compute_dynamics_variability(piece, 0)
    assert variability.changes_count == [126]
    assert variability.total_count == 126
    assert np.isclose(variability.ratio, [1.0]).all()


@pytest.mark.parametrize('difference_level', [1, 20, 40])
def test_series_of_notes_of_three_velocities(difference_level: int):
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
    variability = compute_dynamics_variability(piece, 0, difference_levels=[difference_level])
    assert variability.changes_count == [101]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [101 / 299]).all()


@pytest.mark.parametrize('difference_level', [41, 60, 80])
def test_series_of_notes_of_three_velocities_with_greater_difference_level(difference_level: int):
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
    variability = compute_dynamics_variability(piece, 0, difference_levels=[difference_level])
    assert variability.changes_count == [33]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [33 / 299]).all()


def test_series_of_notes_of_three_velocities_with_too_great_difference_level():
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
    variability = compute_dynamics_variability(piece, 0, difference_levels=[81])
    assert variability.changes_count == [0]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [0 / 299]).all()


def test_series_of_notes_of_three_velocities_with_two_difference_levels():
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
    variability = compute_dynamics_variability(piece, 0, difference_levels=[40, 41])
    assert variability.changes_count == [68, 33]
    assert variability.total_count == 299
    assert np.isclose(variability.ratio, [68 / 299, 33 / 299]).all()
