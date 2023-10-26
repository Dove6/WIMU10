import muspy as mp

def dummy_metric():
    """Dummy metric."""
    pass


def midi_markov(music: mp.Music):
    for track in music.tracks:
        for note in track.notes:
            note.print()
