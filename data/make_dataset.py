"""Scripts to download or generate data"""
import muspy as mp
from argparse import ArgumentParser
from os import makedirs
from pathlib import Path

DATA_RAW_PATH = './data/raw/'
DATASETS = {
    'lakh': mp.LakhMIDIDataset,
    'maestro': mp.MAESTRODatasetV3,
    'nesmdb': mp.NESMusicDatabase,
    'musicnet': mp.MusicNetDataset,
    'emopia': mp.EMOPIADataset,
}


def download_muspy_midi(dataset_name: str):
    """Download a MusPy MIDI dataset specified by name.
    Available datasets:
    * "lakh": mp.LakhMIDIDataset
    * "maestro": mp.MAESTRODatasetV3
    * "nesmdb": mp.NESMusicDatabase
    * "musicnet": mp.MusicNetDataset
    * "emopia": mp.EMOPIADataset
    """
    path = Path(DATA_RAW_PATH + dataset_name)
    if (dataset := DATASETS.get(dataset_name)) is None:
        raise ValueError(f"Expected one of {list(DATASETS.keys())}, got '{dataset_name}'")
    makedirs(path, exist_ok=True)
    dataset(path, download_and_extract=True, cleanup=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dataset', choices=DATASETS.keys(), help='MusPy MIDI dataset to download')
    args = parser.parse_args()
    download_muspy_midi(args.dataset)
