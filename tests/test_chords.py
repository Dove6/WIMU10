import muspy as mp
import numpy as np
from wimu10 import get_chords_list, chords_histogram, chords_transition_matrix

def test_get_chords_case_1() -> None:
    '''
    Note progression case:
    1 -> 1/2/3
    
    Results (found chords):
    [1/2/3]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=500, velocity=100),
        mp.Note(time=1300, pitch=2, duration=100, velocity=100),
        mp.Note(time=1301, pitch=3, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
    
def test_get_chords_case_2() -> None:
    ''' 
    Note progression case:
    1/2 -> 1/2/3/4
    
    Results (found chords):
    [1/2/3/4]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=500, velocity=100),
        mp.Note(time=1001, pitch=2, duration=500, velocity=100),
        mp.Note(time=1300, pitch=3, duration=100, velocity=100),
        mp.Note(time=1301, pitch=4, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_3() -> None:
    ''' 
    Note progression case:
    1/2 -> 1/2/3/4 -> _ -> 5/6/7
    
    Results (found chords):
    [1/2/3/4, 5/6/7]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=500, velocity=100),
        mp.Note(time=1001, pitch=2, duration=500, velocity=100),
        mp.Note(time=1300, pitch=3, duration=100, velocity=100),
        mp.Note(time=1301, pitch=4, duration=99, velocity=100),
        mp.Note(time=1500, pitch=5, duration=500, velocity=100),
        mp.Note(time=1700, pitch=6, duration=100, velocity=100),
        mp.Note(time=1701, pitch=7, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4], [5,6,7]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_4() -> None:
    ''' 
    Note progression case:
    1/2 -> 1/2/3/4 -> _ -> 5/6/7
    
    Results (found chords):
    [1/2/3/4, 5/6/7]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=500, velocity=100),
        mp.Note(time=1001, pitch=2, duration=500, velocity=100),
        mp.Note(time=1300, pitch=3, duration=100, velocity=100),
        mp.Note(time=1301, pitch=4, duration=99, velocity=100),
        mp.Note(time=1700, pitch=5, duration=500, velocity=100),
        mp.Note(time=1900, pitch=6, duration=100, velocity=100),
        mp.Note(time=1901, pitch=7, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3,4], [5,6,7]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords
def test_get_chords_case_5() -> None:
    ''' 
    Note progression case:
    1/2 -> 1/2/3 -> 1/2 -> 1/2/4 -> 1/2 -> 1/2/5
    
    Results (found chords):
    [1/2/3, 1/2/4, 1/2/5]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=1000, velocity=100),
        mp.Note(time=1001, pitch=2, duration=1000, velocity=100),
        mp.Note(time=1300, pitch=3, duration=100, velocity=100),
        mp.Note(time=1500, pitch=4, duration=100, velocity=100),
        mp.Note(time=1700, pitch=5, duration=100, velocity=100),
    ])
    test_case_chords = [[1,2,3], [1,2,4], [1,2,5]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords

def test_get_chords_case_6() -> None:
    ''' 
    Note progression case:
    1/2/10 -> 1/2/3/10 -> 1/2/10 -> 1/2/4/10 -> 1/2/10 -> 1/2/5/10 -> 6
    
    Results (found chords):
    [1/2/10, 1/2/3/10, 1/2/10, 1/2/4/10, 1/2/10, 1/2/5/10]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=1000, velocity=100),
        mp.Note(time=1000, pitch=10, duration=1000, velocity=100),
        mp.Note(time=1001, pitch=2, duration=1000, velocity=100),
        mp.Note(time=1300, pitch=3, duration=100, velocity=100),
        mp.Note(time=1500, pitch=4, duration=100, velocity=100),
        mp.Note(time=1700, pitch=5, duration=100, velocity=100),
        mp.Note(time=2100, pitch=6, duration=100, velocity=100),
    ])
    test_case_chords = [[1,2,10], [1,2,3,10], [1,2,10], [1,2,4,10], [1,2,10], [1,2,5,10]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords

def test_get_chords_case_7() -> None:
    ''' 
    Note progression case:
    1/2/3 -> 1/2/3/4/5 -> 1/2 -> 6/7/8
    
    Results (found chords):
    [1/2/3, 1/2/3/4/5, 6/7/8]  
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=500, velocity=100),
        mp.Note(time=1001, pitch=2, duration=500, velocity=100),
        mp.Note(time=1001, pitch=3, duration=400, velocity=100),
        mp.Note(time=1300, pitch=4, duration=100, velocity=100),
        mp.Note(time=1301, pitch=5, duration=99, velocity=100),
        mp.Note(time=1600, pitch=6, duration=99, velocity=100),
        mp.Note(time=1601, pitch=7, duration=99, velocity=100),
        mp.Note(time=1602, pitch=8, duration=99, velocity=100),
    ])
    test_case_chords = [[1,2,3], [1,2,3,4,5], [6,7,8]]
    result_chords = get_chords_list(test_case)
    assert test_case_chords == result_chords

def test_chords_histogram_case_1() -> None:
    '''
    Note progression case:
    1/2/3 -> 1/2/3 -> 4/5/6
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=100, velocity=100),
        mp.Note(time=1000, pitch=2, duration=100, velocity=100),
        mp.Note(time=1000, pitch=3, duration=100, velocity=100),
        mp.Note(time=1200, pitch=1, duration=100, velocity=100),
        mp.Note(time=1200, pitch=2, duration=100, velocity=100),
        mp.Note(time=1200, pitch=3, duration=100, velocity=100),
        mp.Note(time=1400, pitch=4, duration=100, velocity=100),
        mp.Note(time=1400, pitch=5, duration=100, velocity=100),
        mp.Note(time=1400, pitch=6, duration=100, velocity=100),
    ])
    
    test_case_histogram = {'1/2/3': 2, '4/5/6': 1}
    result_hist = chords_histogram(test_case)
    assert test_case_histogram == result_hist

def test_chords_histogram_case_2() -> None:
    '''
    Note progression case:
    1/2/3 -> 1/2/3 -> 4/5/6 -> 1/2 -> 1/2/3 -> 1/2 -> 1/2/4 -> 1/2 -> 1/2/5

    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=100, velocity=100),
        mp.Note(time=1000, pitch=2, duration=100, velocity=100),
        mp.Note(time=1000, pitch=3, duration=100, velocity=100),
        
        mp.Note(time=1200, pitch=1, duration=100, velocity=100),
        mp.Note(time=1200, pitch=2, duration=100, velocity=100),
        mp.Note(time=1200, pitch=3, duration=100, velocity=100),
        
        mp.Note(time=1400, pitch=4, duration=100, velocity=100),
        mp.Note(time=1400, pitch=5, duration=100, velocity=100),
        mp.Note(time=1400, pitch=6, duration=100, velocity=100),
        
        mp.Note(time=2000, pitch=1, duration=1000, velocity=100),
        mp.Note(time=2001, pitch=2, duration=1000, velocity=100),
        mp.Note(time=2300, pitch=3, duration=100, velocity=100),
        mp.Note(time=2500, pitch=4, duration=100, velocity=100),
        mp.Note(time=2700, pitch=5, duration=100, velocity=100),
    ])
    
    test_case_histogram = {'1/2/3': 3, '4/5/6': 1, '1/2/4':1, '1/2/5':1}
    result_hist = chords_histogram(test_case)
    assert test_case_histogram == result_hist
    
def test_chords_histogram_piano_notation() -> None:
    '''
    Note progression case:
    48/50/52 -> 48/50/52 -> 61/64/65
    
    Piano note case:
    C3/D3/E3 -> C3/D3/E3 -> C#4/E4/F4
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=48, duration=100, velocity=100),
        mp.Note(time=1000, pitch=50, duration=100, velocity=100),
        mp.Note(time=1000, pitch=52, duration=100, velocity=100),
        mp.Note(time=1200, pitch=48, duration=100, velocity=100),
        mp.Note(time=1200, pitch=50, duration=100, velocity=100),
        mp.Note(time=1200, pitch=52, duration=100, velocity=100),
        mp.Note(time=1400, pitch=61, duration=100, velocity=100),
        mp.Note(time=1400, pitch=64, duration=100, velocity=100),
        mp.Note(time=1400, pitch=65, duration=100, velocity=100),
    ])
    
    test_case_histogram = {'C3/D3/E3': 2, 'C#4/E4/F4': 1}
    result_hist = chords_histogram(test_case, "piano")
    assert test_case_histogram == result_hist
    
def test_chords_transition_matrix_case_1() -> None:
    '''
    Note progression case:
    1/2/3 -> 1/2/3 -> 4/5/6
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=100, velocity=100),
        mp.Note(time=1000, pitch=2, duration=100, velocity=100),
        mp.Note(time=1000, pitch=3, duration=100, velocity=100),
        mp.Note(time=1200, pitch=1, duration=100, velocity=100),
        mp.Note(time=1200, pitch=2, duration=100, velocity=100),
        mp.Note(time=1200, pitch=3, duration=100, velocity=100),
        mp.Note(time=1400, pitch=4, duration=100, velocity=100),
        mp.Note(time=1400, pitch=5, duration=100, velocity=100),
        mp.Note(time=1400, pitch=6, duration=100, velocity=100),
    ])
    
    unique_chords = {'1/2/3': 0, '4/5/6': 1}
    chord_matrix = np.array([[0.5, 0.5],[0. , 0. ]])
    results_chords, results_matrix = chords_transition_matrix(test_case)
    assert unique_chords == results_chords
    assert np.array_equal(results_matrix, chord_matrix)

def test_chords_transition_matrix_case_2() -> None:
    '''
    Note progression case:
    1/2/3 -> 1/2/3 -> 4/5/6 -> 1/2 -> 1/2/3 -> 1/2 -> 1/2/4 -> 1/2 -> 1/2/5

    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=1, duration=100, velocity=100),
        mp.Note(time=1000, pitch=2, duration=100, velocity=100),
        mp.Note(time=1000, pitch=3, duration=100, velocity=100),
        
        mp.Note(time=1200, pitch=1, duration=100, velocity=100),
        mp.Note(time=1200, pitch=2, duration=100, velocity=100),
        mp.Note(time=1200, pitch=3, duration=100, velocity=100),
        
        mp.Note(time=1400, pitch=4, duration=100, velocity=100),
        mp.Note(time=1400, pitch=5, duration=100, velocity=100),
        mp.Note(time=1400, pitch=6, duration=100, velocity=100),
        
        mp.Note(time=2000, pitch=1, duration=1000, velocity=100),
        mp.Note(time=2001, pitch=2, duration=1000, velocity=100),
        mp.Note(time=2300, pitch=3, duration=100, velocity=100),
        mp.Note(time=2500, pitch=4, duration=100, velocity=100),
        mp.Note(time=2700, pitch=5, duration=100, velocity=100),
    ])
    
    unique_chords = {'1/2/3': 0, '4/5/6': 1, '1/2/4': 2, '1/2/5': 3}
    chord_matrix = np.array([[1/3 ,1/3 ,1/3 ,0],
                            [1, 0 ,0 ,0],
                            [0, 0 ,0 ,1],
                            [0, 0 ,0 ,0],])
    results_chords, results_matrix = chords_transition_matrix(test_case)
    assert unique_chords == results_chords
    assert np.array_equal(results_matrix, chord_matrix)
    
def test_chords_transition_matrix_piano_notation() -> None:
    '''
    Note progression case:
    48/50/52 -> 48/50/52 -> 61/64/65
    
    Piano note case:
    C3/D3/E3 -> C3/D3/E3 -> C#4/E4/F4
    '''
    test_case = mp.Track(notes= [
        mp.Note(time=1000, pitch=48, duration=100, velocity=100),
        mp.Note(time=1000, pitch=50, duration=100, velocity=100),
        mp.Note(time=1000, pitch=52, duration=100, velocity=100),
        mp.Note(time=1200, pitch=48, duration=100, velocity=100),
        mp.Note(time=1200, pitch=50, duration=100, velocity=100),
        mp.Note(time=1200, pitch=52, duration=100, velocity=100),
        mp.Note(time=1400, pitch=61, duration=100, velocity=100),
        mp.Note(time=1400, pitch=64, duration=100, velocity=100),
        mp.Note(time=1400, pitch=65, duration=100, velocity=100),
    ])
    
    test_case_chords = {'C3/D3/E3': 0, 'C#4/E4/F4': 1}
    results_chords, _ = chords_transition_matrix(test_case, "piano")
    assert test_case_chords == results_chords