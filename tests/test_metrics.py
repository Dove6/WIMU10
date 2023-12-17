import muspy as mp
from wimu10 import dummy_metric
from wimu10 import get_chords_list

def test_dummy_metric():
    ''' Test 1 '''
    dummy_metric()
def test_get_chords_case_1():
    ''' Test 1 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=500, velocity=100),
        mp.Note(time = 1300, pitch= 2, duration=100, velocity=100),
        mp.Note(time = 1301, pitch= 3, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_2():
    ''' Test 2 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=500, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=500, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1301, pitch= 4, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_3():
    ''' Test 3 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=500, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=500, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1301, pitch= 4, duration=99, velocity=100),
        mp.Note(time = 1500, pitch= 5, duration=500, velocity=100),
        mp.Note(time = 1700, pitch= 6, duration=100, velocity=100),
        mp.Note(time = 1701, pitch= 7, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4], [5,6,7]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_4():
    ''' Test 4 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=500, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=500, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1301, pitch= 4, duration=99, velocity=100),
        mp.Note(time = 1700, pitch= 5, duration=500, velocity=100),
        mp.Note(time = 1900, pitch= 6, duration=100, velocity=100),
        mp.Note(time = 1901, pitch= 7, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4], [5,6,7]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_5():
    ''' Test 5 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=1000, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=1000, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1500, pitch= 4, duration=100, velocity=100),
        mp.Note(time = 1700, pitch= 5, duration=100, velocity=100),
    ])
    test_case_chords = [[1,2,3], [1,2,4], [1,2,5]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords

def test_get_chords_case_6():
    ''' Test 6 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=1000, velocity=100),
        mp.Note(time = 1000, pitch= 10, duration=1000, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=1000, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1500, pitch= 4, duration=100, velocity=100),
        mp.Note(time = 1700, pitch= 5, duration=100, velocity=100),
        mp.Note(time = 2100, pitch= 5, duration=100, velocity=100),
    ])
    test_case_chords = [[1,2,10], [1,2,3,10], [1,2,10], [1,2,4,10], [1,2,10], [1,2,5,10]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords

def test_get_chords_case_7() -> None:
    ''' Test 7 '''
    test_case = mp.Track(notes= [
        mp.Note(time = 1000, pitch= 1, duration=500, velocity=100),
        mp.Note(time = 1001, pitch= 2, duration=500, velocity=100),
        mp.Note(time = 1001, pitch= 10, duration=500, velocity=100),
        mp.Note(time = 1300, pitch= 3, duration=100, velocity=100),
        mp.Note(time = 1301, pitch= 4, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,10],[1,2,3,4,10]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
