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
    readable_output: str = "midi", 
    error_frame: int = 75
):
    """
    Returns histogram of chords.
    
    track: Track to retrive the chord histogram from.
    readable_output: Whether to output the given chords in MIDI number format or key notations for piano.
    error_frame: How much time can pass between single notes for them to still me in the same chord. 
    """
    chords = get_chords_list(track, error_frame)
    chord_hist:dict = {}
    
    if readable_output == "midi":
        str_chords = midi_chords(chords)
    elif readable_output == "piano":
        str_chords =  piano_chords(chords)
    else:
        return Exception("Format not supported")
    
    for chord in str_chords:
        if chord in chord_hist:
            chord_hist[chord] += 1
        else:
            chord_hist[chord] = 1
    return chord_hist

def chords_transition_matrix(
    track: mp.Track,
    readable_output: str = "midi", 
    error_frame: int = 75
):
    """
    Calculates the transition matrix for the chords in a track.
    Returns dictionary of unique chords and transition matrix.
    
    track: Track to retrive the chord histogram from.
    readable_output: Whether to output the given chords in MIDI number format or key notations for piano.
    error_frame: How much time can pass between single notes for them to still me in the same chord. 
    """
    chords = get_chords_list(track, error_frame)
    if readable_output == "midi":
        str_chords = midi_chords(chords)
    elif readable_output == "piano":
        str_chords =  piano_chords(chords)
    else:
        return Exception("Format not supported")
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

def midi_chords(chords_list:list[list[int]]) -> list[str]:
    return [ '/'.join(map(str,chord)) for chord in chords_list]

def piano_chords(chords_list:list[list[int]]) -> list[str]:
    return [ '/'.join([map_midi_to_piano(midi_number) for midi_number in chord]) for chord in chords_list]

def map_midi_to_piano(midi_note:int):
    notes_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if 21 <= midi_note <= 108:
        return notes_mapping[midi_note%12] + str(midi_note//12 - 1)
    else:
        return Exception("midi_number beyond piano bounds")

def get_unique_chords(chords_list:list[str]):
    chord_id = 0
    unique_chords:dict = {}
    for chord in chords_list:
        if unique_chords.get(chord) is None:
            unique_chords[chord] = chord_id
            chord_id += 1
    return unique_chords
    
def get_chords_list(
    track: mp.Track,
    error_frame: int = 75
) -> list[list[int]]:
    """
    Returns list of chords within a track.
    The returned chords are a lists of MIDI note numbers.
    
    track: Track to retrive the chords list from.
    error_frame: How much time can pass between single notes for them to still me in the same chord. 
    """
    notes = track.notes
    frame_end: int = 0
    curr_played_notes: list[mp.Note] = []
    chord_list: list[list[int]] = []

    for curr_note_id in range(0, len(notes)):
        
        # Deleting stale notes that are not longer playing
        fresh_notes =[]
        smallest_pause = 0
        for note in curr_played_notes:
            if (note.time + note.duration) > notes[curr_note_id].time:
                fresh_notes.append(note)
            else:
                smallest_pause = max(smallest_pause, note.time + note.duration)
        curr_played_notes[:] = fresh_notes
        
        # Adding chords for instances of subtarcting and adding notes, ex: D3/E3/F3/G3 -> D3/E3/F3 -> D3/E3/F3/A3/B3
        if smallest_pause > 0 and len(curr_played_notes) >=3 and (notes[curr_note_id].time - smallest_pause > error_frame ):
            add_chord_to_list(chord_list, curr_played_notes)
        
        # Adding notes until we have a chord
        if len(curr_played_notes) < 2:
            curr_played_notes.append(notes[curr_note_id])
            
        # Adding a chord for when more than 2 notes are played simultaneously.
        else: 
            if notes[curr_note_id].time > frame_end:
                frame_end = notes[curr_note_id].time + error_frame
            curr_played_notes.append(notes[curr_note_id])
            if (len(notes) -1) == curr_note_id or notes[curr_note_id+1].time > frame_end :
                add_chord_to_list(chord_list, curr_played_notes)
    return chord_list

def add_chord_to_list(list_of_chords: list[list[int]], curr_notes:list[mp.Note]):
    new_chord = []
    for chord in curr_notes:
        new_chord.append(chord.pitch)
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