from wimu10 import compute_self_similarity


import muspy as mp


RESOLUTION_MUL = 1 / 4
MIN_LENGTH_MUL = 1 / 40


def test_only_repeats():
    music = mp.read_midi('tests/data/only_repeats.mid')
    resolution = int(music.resolution * RESOLUTION_MUL)
    min_length = int(music.resolution * MIN_LENGTH_MUL)
    score = compute_self_similarity(music.tracks[0], resolution=resolution, min_length=min_length)
    assert score == 1.0


def test_some_repeats():
    music = mp.read_midi('tests/data/some_repeats.mid')
    resolution = int(music.resolution * RESOLUTION_MUL)
    min_length = int(music.resolution * MIN_LENGTH_MUL)
    score = compute_self_similarity(music.tracks[0], resolution=resolution, min_length=min_length)
    assert abs(score - 0.5) < 1e-1


def test_no_repeats():
    music = mp.read_midi('tests/data/no_repeats.mid')
    resolution = int(music.resolution * RESOLUTION_MUL)
    min_length = int(music.resolution * MIN_LENGTH_MUL)
    score = compute_self_similarity(music.tracks[0], resolution=resolution, min_length=min_length)
    assert score == 0.0
