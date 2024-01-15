import muspy as mp
import numpy as np


def chords_histogram(
    track: mp.Track,
    readable_output: str = "midi",
    error_frame: int = 75
) -> dict[str, int] or None:
    """
    Calculates and returns the histogram of chords in the track.
    Returns the values in MIDI note format or in piano key notation.
    Returns 'None' in case of 'readable_output' value.

    track: Track to retrive the chord histogram from.
    readable_output: Whether to output the given chords
    in MIDI number format or piano key notation.
    error_frame: How much time can pass between single notes for them to still me in the same chord.
    Due to the fact that notes can be inputed with delays(because of the playing style, human or machine error).
    This value is given to prevent a single bigger chord, where separte notes are played with slight delays and have different timestamps.
    At the time of programming and testing the initial value '75' was set and tested on the 'musicnet' dataset.
    """
    chords = get_chords_list(track, error_frame)
    chord_hist:dict = {}

    if readable_output == "midi":
        str_chords = _midi_chords(chords)
    elif readable_output == "piano":
        str_chords =  _piano_chords(chords)
    else:
        return None

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
) -> (dict[str, int], np.ndarray[float]):
    """
    Calculates the transition matrix for the chords in a track.
    Returns dictionary of unique chords and a transition matrix.
    Returns 'None' in case of 'readable_output' value.

    track: Track to retrive the chord histogram from.
    readable_output: Whether to output the given chords
    in MIDI number format or piano key notation.
    error_frame: How much time can pass between single notes for them to still me in the same chord.
    Due to the fact that notes can be inputed with delays(because of the playing style, human or machine error).
    This value is given to prevent a single bigger chord, where separte notes are played with slight delays and have different timestamps.
    At the time of programming and testing the initial value '75' was set and tested on the 'musicnet' dataset.
    """
    chords = get_chords_list(track, error_frame)
    if readable_output == "midi":
        str_chords = _midi_chords(chords)
    elif readable_output == "piano":
        str_chords =  _piano_chords(chords)
    else:
        return None

    chords_dict = _get_unique_chords(str_chords)

    # Unique chords count
    u_count = len(chords_dict)

    # Generate transition matrix
    matrix = np.zeros((u_count,u_count))

    for (i,j) in zip(str_chords, str_chords[1:]):
        matrix[chords_dict[i]][chords_dict[j]] += 1

    # Convert to probability
    for row in matrix:
        s = sum(row)
        if s > 0:
            row[:] = [f/s for f in row]
    return chords_dict, matrix

def get_chords_list(
    track: mp.Track,
    error_frame: int = 75
) -> list[list[int]]:
    """
    Returns list of chords within a track.
    The returned chords are lists of MIDI note numbers.

    track: Track to retrive the chords list from.
    error_frame: How much time can pass between single notes for them to still me in the same chord.
    Due to the fact that notes can be inputed with delays(because of the playing style, human or machine error).
    This value is given to prevent a single bigger chord, where separte notes are played with slight delays and have different timestamps.
    At the time of programming and testing the initial value '75' was set and tested on the 'musicnet' dataset.
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

        # Adding chords for instances of subtarcting and adding notes,
        # ex: D3/E3/F3/G3 -> D3/E3/F3 -> D3/E3/F3/A3/B3
        if smallest_pause > 0 and len(curr_played_notes) >=3 and (notes[curr_note_id].time - smallest_pause > error_frame):
            _add_chord_to_list(chord_list, curr_played_notes)

        # Adding notes until we have a chord
        if len(curr_played_notes) < 2:
            curr_played_notes.append(notes[curr_note_id])

        # Adding a chord for when more than 2 notes are played simultaneously.
        else:
            if notes[curr_note_id].time > frame_end:
                frame_end = notes[curr_note_id].time + error_frame
            curr_played_notes.append(notes[curr_note_id])
            if (len(notes) -1) == curr_note_id or notes[curr_note_id+1].time > frame_end :
                _add_chord_to_list(chord_list, curr_played_notes)
    return chord_list

def _add_chord_to_list(list_of_chords: list[list[int]], curr_notes:list[mp.Note]):
    new_chord = []
    for chord in curr_notes:
        new_chord.append(chord.pitch)
    new_chord.sort()
    list_of_chords.append(new_chord)

def _get_unique_chords(chords_list:list[str]):
    chord_id = 0
    unique_chords:dict = {}
    for chord in chords_list:
        if unique_chords.get(chord) is None:
            unique_chords[chord] = chord_id
            chord_id += 1
    return unique_chords

def _midi_chords(chords_list:list[list[int]]) -> list[str]:
    return [ '/'.join(map(str,chord)) for chord in chords_list]

def _piano_chords(chords_list:list[list[int]]) -> list[str]:
    return [ '/'.join([_map_midi_to_piano(midi_number) for midi_number in chord])
            for chord in chords_list]

def _map_midi_to_piano(midi_note:int):
    notes_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    if 21 <= midi_note <= 108:
        return notes_mapping[midi_note%12] + str(midi_note//12 - 1)
    else:
        return Exception("midi_number beyond piano bounds")
