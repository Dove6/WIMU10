from collections.abc import Callable, Collection
from typing import Optional

import muspy as mp
import numpy as np

Notes = Collection[int]
Comparator = Callable[[Notes, Notes], int]


def dummy_metric():
    """Dummy metric."""
    pass


def chords_histogram(
    track: mp.Track,
    error_frame: int = 75
):
    """
    Returns histogram of chords.
    
    track: Track to retrive the chord histogram from.
    error_frame: How much time can pass between single notes for them to still me in the same chord. 
    """
    chords = get_chords_list(track, error_frame)
    chord_hist:dict = {}
    
    chords = stringify_chords(chords)
    
    for chord in chords:
        if chord in chord_hist:
            chord_hist[chord] += 1
        else:
            chord_hist[chord] = 1
    return chord_hist

def chords_transition_matrix(
    track: mp.Track,
    error_frame: int = 75
):
    """
    Calculates the transition matrix for the chords in a track.
    Returns dictionary of unique chords and transition matrix.
    """
    chords = get_chords_list(track, error_frame)
    str_chords = stringify_chords(chords)
    chords_dict = get_unique_chords(str_chords)
    
    # Unique chords count
    u_count = len(chords_dict)
    
    # Generate transition matrix
    M = np.zeros((u_count,u_count))
    
    for (i,j) in zip(str_chords, str_chords[1:]):
        M[chords_dict[i]][chords_dict[j]] += 1
    
    # Convert to probability
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return chords_dict, M

def stringify_chords(chords_list:list[list[int]]) -> list[str]:
    return [ '/'.join(map(str,chord)) for chord in chords_list]

def get_unique_chords(chords_list:list[str]):
    chord_id = 0
    unique_chords:dict = {}
    for chord in chords_list:
        if unique_chords.get(chord) is None:
            unique_chords[chord] = chord_id
            chord_id += 1
    return unique_chords
    

# Case not done-> Two notes are played for long and then halfway through two more notes are added until the end, 
# That indeed creates a cord.
def get_chords_list(
    track: mp.Track,
    error_frame: int = 75
) -> list[list[int]]:
    """
    Returns list of all found chords within the track.
    
    track: Track to retrive the chords list from.
    error_frame: How much time can pass between single notes for them to still me in the same chord. 
    """
    notes_list = track.notes
    time_max:int = 0
    chord_list: list[list[int]] = []#potencjalnie zmień na chord
    possible_chord: list[int] = []
    for id_note in range(0, len(notes_list) - 1):
        
        if notes_list[id_note].time > time_max:
            time_max = notes_list[id_note].time + error_frame
            complete_chord(chord_list, possible_chord)   
            possible_chord = []
        possible_chord.append(notes_list[id_note].pitch)
        if id_note == len(notes_list) -1:
            complete_chord(chord_list, possible_chord)            
    return chord_list

def complete_chord(list_of_chords: list[list[int]], new_chord:list[int]) -> None:
    if len(new_chord) > 2:
        new_chord.sort()
        list_of_chords.append(new_chord)

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
