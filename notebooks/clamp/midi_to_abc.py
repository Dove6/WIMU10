from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path
from typing import List, Optional
from threading import Lock
import subprocess
from timeit import default_timer as timer
from datetime import timedelta


class Counter:
    """
    Helper class to track progress amongst many threads.
    """

    def __init__(self, total: int):
        self.total = total
        self.complete = 0
        self.successes = 0
        self.failures = 0
        self.lock = Lock()

    def add_success(self):
        with self.lock:
            self.complete += 1
            self.successes += 1
            print(f'Completed {self.complete: >4} / {self.total: <4} (success)')

    def add_failure(self):
        with self.lock:
            self.complete += 1
            self.failures += 1
            print(f'Completed {self.complete: >4} / {self.total: <4} (failure)')


def batch_midi_to_abc(srcs: List[Path], dsts: List[Path], max_workers: Optional[int] = None):
    """
    Convert all MIDI source files `srcs` to ABC destination files `dsts`.
    Lengths of `srcs` and `dsts` must match.
    """
    assert len(srcs) == len(dsts)

    counter = Counter(len(srcs))
    start = timer()
    with ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(try_midi_to_abc, src, dst, counter) for (src, dst) in zip(srcs, dsts)]
        wait(futures)
    end = timer()
    delta = f'{timedelta(seconds=end - start)}'
    print('┌───────────┬────────────────┐')
    print(f'│  Elapsed  │ {delta: <9} │')
    print('├───────────┼────────────────┤')
    print(f'│ Successes │  {counter.successes: >4} / {counter.total: <4}   │')
    print(f'│  Failures │  {counter.failures: >4} / {counter.total: <4}   │')
    print('└───────────┴────────────────┘')


def try_midi_to_abc(src: Path, dst: Path, counter: Counter):
    """
    Fail-safe MIDI to ABC.
    For use in batch.
    """
    try:
        dst.unlink(missing_ok=True)
        dst.parent.mkdir(parents=True, exist_ok=True)
        midi_to_abc(src, dst)
        counter.add_success()
    except Exception as e:
        print(f'Failed to process `{src}`: {e}')
        counter.add_failure()


def midi_to_abc(src: Path, dst: Path):
    """
    Conversion of one MIDI file to one ABC file.
    """
    dst.touch(exist_ok=False)
    subprocess.Popen(f'notebooks/clamp/midi2abc.exe -s -o "{dst}" "{src}"', stdout=subprocess.PIPE)


def main(input_dir: Path, output_dir: Path, max_workers: Optional[int] = None):
    """
    Convert all MIDI files from `input_dir` to appropriate ABC files in `output_dir`.
    `max_workers` allows changing the max of threads used.
    """
    srcs = list(input_dir.glob('**/*.midi'))
    dsts = [output_dir.joinpath(*src.parts[len(input_dir.parts) : -1]).joinpath(f'{src.stem}.abc') for src in srcs]
    batch_midi_to_abc(srcs, dsts, max_workers)


if __name__ == '__main__':
    main(Path('data/raw/maestro/maestro-v3.0.0'), Path('data/raw/maestro/maestro-v3.0.0-abc'))
