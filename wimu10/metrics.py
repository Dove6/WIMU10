import muspy as mp

def dummy_metric():
    """Dummy metric."""
    pass


def midi_markov(track: mp.Track):
    notess = []
    print(track.notes)
    for t in range(0, 160000, 100):
        notes = []
        for note in track.notes:
            if note.start <= t and t <= note.end:
                notes.append(note)
        notess.append(notes)
    print(notess)
