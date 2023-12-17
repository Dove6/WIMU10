from collections.abc import Callable, Collection
from typing import Optional

import muspy as mp
import numpy as np

Notes = Collection[int]
Comparator = Callable[[Notes, Notes], int]


# Defaults as in Logic Pro
DEFAULT_DYNAMICS_LEVELS = [
    16,  # ppp
    33,  # pp
    49,  # p
    64,  # mp
    80,  # mf
    96,  # f
    112,  # ff
    127,  # fff
]


def dummy_metric():
    """Dummy metric."""
    pass


def score_matching_notes(a: Notes, b: Notes) -> int:
    score = 0
    for c in a:
        if c in b:
            score += 1
    return score


def score_perfect_match(a: Notes, b: Notes) -> int:
    return 1 if a == b else 0


def self_similarity(
    track: mp.Track,
    resolution: int = 16,
    squash: bool = True,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
    comparison_fn: Comparator = score_perfect_match,
):
    """
    Calculates the top bottom of self similarity matrix.
    The diagonal is unset and the top triangle is symmetrical.

    track: Track to calculate the metric on.
    resolution: How dense the comparison is.
    squash: Whether to squash pitch to a single octave
    track_start: Override for track start
    track_end: Override for trask end
    comparison_fn: Comparison function for 2 points in time

    returns: Self-similarity matrix
    """
    # Find bounds
    track_start = track_start or min(note.start for note in track.notes)
    track_end = track_end or max(note.end for note in track.notes)
    # Represent as notes playing at specific times
    timestamps: list[list[int]] = []
    for t in range(track_start, track_end, resolution):
        notes: list[int] = []
        for note in track.notes:
            if note.start <= t and t <= note.end:
                pitch = note.pitch
                if squash:
                    pitch = pitch % 12
                notes.append(pitch)
        timestamps.append(notes)
    # Compare all notes, skip identical and reversed pairs
    # The following matrix is computed, `_` indicate skipped comparisons
    #   0 1 2
    # 0 _ _ _
    # 1 x _ _
    # 2 x x _
    timestamp_count = len(timestamps)
    scores = np.zeros((timestamp_count, timestamp_count))
    for i, a in enumerate(timestamps):
        for j, b in enumerate(timestamps[:i]):
            scores[i, j] += comparison_fn(a, b)
    return scores


def compute_dynamics_histogram(
    music: mp.Music,
    track_idx: int,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the histogram of velocities of all notes in the track. The range of velocity values in MIDI is 0-127.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: MIDI velocity histogram for the chosen track.
    """
    track = music.tracks[track_idx]
    velocities_hist = [0] * 128
    for note in _iterate_over_notes(track, resolution, track_start, track_end):
        velocities_hist[note.velocity] += 1
    return velocities_hist


def compute_dynamics_levels_histogram(
    music: mp.Music,
    track_idx: int,
    dynamics_levels: list[int] = None,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the histogram of (configurable) dynamics levels of all notes in the track.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    dynamics_levels: List of starting values for consecutive dynamic levels. The values must be in range 0-127.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: Dynamics level histogram for the chosen track.
    """
    if dynamics_levels is None:
        dynamics_levels = DEFAULT_DYNAMICS_LEVELS
    else:
        dynamics_levels = sorted(dynamics_levels)
        if dynamics_levels[0] < 0 or dynamics_levels[-1] > 127:
            raise ValueError('Dynamic levels out of range (0-127)')
    track = music.tracks[track_idx]
    dynamics_level_hist = [0] * len(dynamics_levels)
    for note in _iterate_over_notes(track, resolution, track_start, track_end):
        dynamic_level_idx = -1
        for dynamics_level in dynamics_levels:
            if dynamics_level > note.velocity:
                break
            dynamic_level_idx += 1
        if dynamic_level_idx >= 0:
            dynamics_level_hist[dynamic_level_idx] += 1
    return dynamics_level_hist


def compute_dynamics_transition_matrix(
    music: mp.Music,
    track_idx: int,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the transition matrix for velocities of all notes in the track. The range of velocity values in MIDI is 0-127.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: MIDI velocity transition matrix for the chosen track.
    """
    track = music.tracks[track_idx]
    velocity_transition_matrix = np.zeros((128, 128), dtype=int)
    previous_velocity = None
    for note in _iterate_over_top_notes_in_groups(track, resolution, track_start, track_end):
        if previous_velocity is not None:
            velocity_transition_matrix[previous_velocity][note.velocity] += 1
        previous_velocity = note.velocity
    return velocity_transition_matrix


def compute_dynamics_levels_transition_matrix(
    music: mp.Music,
    track_idx: int,
    dynamics_levels: list[int] = None,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the transition matrix for (configurable) dynamics levels of all notes in the track.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    dynamics_levels: List of starting values for consecutive dynamic levels. The values must be in range 0-127.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: Dynamics level transition matrix for the chosen track.
    """
    if dynamics_levels is None:
        dynamics_levels = DEFAULT_DYNAMICS_LEVELS
    else:
        dynamics_levels = sorted(dynamics_levels)
        if dynamics_levels[0] < 0 or dynamics_levels[-1] > 127:
            raise ValueError('Dynamic levels out of range (0-127)')
    track = music.tracks[track_idx]
    level_transition_matrix = np.zeros((len(dynamics_levels), len(dynamics_levels)), dtype=int)
    previous_level = None
    for note in _iterate_over_top_notes_in_groups(track, resolution, track_start, track_end):
        current_level = -1
        for dynamics_level in dynamics_levels:
            if dynamics_level > note.velocity:
                break
            current_level += 1
        if current_level < 0:
            continue
        if previous_level is not None:
            level_transition_matrix[previous_level][current_level] += 1
        previous_level = current_level
    return level_transition_matrix


def compute_dynamics_variability(
    music: mp.Music,
    track_idx: int,
    difference_levels: list[int] = None,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the ratio of changes in velocity between consecutive top-level notes to all top-level notes in the track. The range of velocity values in MIDI is 0-127.
    Top-level note is the note that has the highest pitch of all notes played simultaneously in the given moment.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    difference_levels: List of starting values for consecutive levels of absolute differences between velocities. The values must be in range 1-127.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: Ratio of velocity changes for the chosen track.
    """
    if difference_levels is None:
        difference_levels = [1]
    else:
        difference_levels = sorted(difference_levels)
        if difference_levels[0] < 1 or difference_levels[-1] > 127:
            raise ValueError('Difference levels out of range (1-127)')
    track = music.tracks[track_idx]
    note_group_count = 0
    velocity_change_counts = [0] * len(difference_levels)
    previous_velocity = None
    for note in _iterate_over_top_notes_in_groups(track, resolution, track_start, track_end):
        note_group_count += 1
        if note.velocity != previous_velocity and previous_velocity is not None:
            difference = abs(note.velocity - previous_velocity)
            difference_level_index = -1
            for difference_level in difference_levels:
                if difference_level > difference:
                    break
                difference_level_index += 1
            if difference_level_index >= 0:
                velocity_change_counts[difference_level_index] += 1
        previous_velocity = note.velocity
    return {
        'ratio': [velocity_change_count / note_group_count for velocity_change_count in velocity_change_counts],
        'changes_count': velocity_change_counts,
        'total_count': note_group_count,
    }


def compute_dynamics_levels_variability(
    music: mp.Music,
    track_idx: int,
    dynamics_levels: list[int] = None,
    difference_levels: list[int] = None,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    """
    Calculates the ratio of changes in (configurable) dynamics levels between consecutive top-level notes to all top-level notes in the track.
    Top-level note is the note that has the highest pitch of all notes played simultaneously in the given moment.

    music: Piece of music containing the track.
    track_idx: The index of the track to calculate the metric on.
    dynamics_levels: List of starting values for consecutive dynamic levels. The values must be in range 0-127.
    difference_levels: List of starting values for consecutive levels of absolute differences between velocities. The values must be in range 1-127.
    resolution: How dense the time scale is.
    track_start: Override for track start.
    track_end: Override for trask end.

    returns: Ratio of dynamics levels changes for the chosen track.
    """
    if dynamics_levels is None:
        dynamics_levels = DEFAULT_DYNAMICS_LEVELS
    else:
        dynamics_levels = sorted(dynamics_levels)
        if dynamics_levels[0] < 0 or dynamics_levels[-1] > 127:
            raise ValueError('Dynamic levels out of range (0-127)')
    if difference_levels is None:
        difference_levels = [1, 3]
    else:
        difference_levels = sorted(difference_levels)
        if difference_levels[0] < 1:
            raise ValueError('Difference levels out of range (1-unrestricted)')
    track = music.tracks[track_idx]
    note_group_count = 0
    velocity_change_counts = [0] * len(difference_levels)
    previous_level = None
    for note in _iterate_over_top_notes_in_groups(track, resolution, track_start, track_end):
        note_group_count += 1
        current_level = -1
        for dynamics_level in dynamics_levels:
            if dynamics_level > note.velocity:
                break
            current_level += 1
        if current_level < 0:
            continue
        if current_level != previous_level and previous_level is not None:
            difference = abs(current_level - previous_level)
            difference_level_index = -1
            for difference_level in difference_levels:
                if difference_level > difference:
                    break
                difference_level_index += 1
            if difference_level_index >= 0:
                velocity_change_counts[difference_level_index] += 1
        previous_level = current_level
    return {
        'ratio': [velocity_change_count / note_group_count for velocity_change_count in velocity_change_counts],
        'changes_count': velocity_change_counts,
        'total_count': note_group_count,
    }


def _iterate_over_notes(
    track: mp.Track,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    # Find bounds
    track_start = track_start or min(note.start for note in track.notes)
    track_end = track_end or max(note.end for note in track.notes)
    # Represent as notes playing at specific times
    for t in range(track_start, track_end, resolution):
        for note in track.notes:
            if note.start <= t and t <= note.end:
                yield note


def _iterate_over_note_groups(
    track: mp.Track,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    # Find bounds
    track_start = track_start or min(note.start for note in track.notes)
    track_end = track_end or max(note.end for note in track.notes)
    # Represent as notes playing at specific times
    for t in range(track_start, track_end, resolution):
        notes: list[mp.Note] = []
        for note in track.notes:
            if note.start <= t and t <= note.end:
                notes.append(note)
        if len(notes) > 0:
            yield notes


def _iterate_over_top_notes_in_groups(
    track: mp.Track,
    resolution: int = 16,
    track_start: Optional[int] = None,
    track_end: Optional[int] = None,
):
    for note_group in _iterate_over_note_groups(track, resolution, track_start, track_end):
        yield max(note_group, key=lambda note: note.pitch)
