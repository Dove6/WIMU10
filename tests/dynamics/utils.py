import muspy as mp
import numpy as np
import numpy.typing as npt
from typing import Callable, Optional, Union, cast


def create_sparse_array(length: int, default_value: int, entries: list[tuple[int, int]]) -> list[int]:
    arr = [default_value for _ in range(length)]
    for index, value in entries:
        arr[index] = value
    return arr


def create_sparse_matrix(size: int, default_value: int, entries: list[tuple[tuple[int, int], int]]) -> npt.NDArray[np.int_]:
    mat = np.ones((size, size), dtype=int) * default_value
    for index, value in entries:
        mat[index] = value
    return mat


def create_track_going_up(
    notes_count: int,
    pitch_bounds: tuple[int, int],
    time_func: Optional[Callable[[int], int]] = None,
    duration_func: Optional[Union[Callable[[int], int], int]] = None,
    volume_func: Optional[Union[Callable[[int], int], int]] = None,
) -> mp.Track:
    if pitch_bounds[0] > pitch_bounds[1]:
        pitch_bounds = (pitch_bounds[1], pitch_bounds[0])
    if time_func is None:
        time_func = lambda index: index * 128  # noqa: E731
    if duration_func is None or isinstance(duration_func, int):
        duration_value = duration_func or 1
        duration_func = lambda _: cast(int, duration_value)  # noqa: E731
    if volume_func is None or isinstance(volume_func, int):
        volume_value = volume_func or 100
        volume_func = lambda _: cast(int, volume_value)  # noqa: E731
    duration_func = cast(Callable[[int], int], duration_func)
    volume_func = cast(Callable[[int], int], volume_func)
    pitch_modulo = pitch_bounds[1] - pitch_bounds[0] + 1
    return mp.Track(
        notes=[
            mp.Note(time_func(i), pitch_bounds[0] + i % pitch_modulo, duration_func(i), volume_func(i))
            for i in range(notes_count)
        ]
    )
