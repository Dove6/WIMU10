# CLaMP: Contrastive Language-Music Pre-training for Cross-Modal Symbolic Music Information Retrieval
# Shangda Wu and Dingyao Yu and Xu Tan and Maosong Sun, 2023
# Forked from https://github.com/microsoft/muzic/blob/main/clamp/clamp.py
# Licensed under MIT

# Modified as following:
# - removed inference,
# - hardwired "music" model,
# - used ABC directly (instead of MusicXML),
# - added in/out directory arguments (removed other ones),
# - added music embedding stored in JSON.

import argparse
import subprocess
from .utils import *
from transformers import AutoTokenizer
from pathlib import Path
from json import dump

if torch.cuda.is_available():
    device = torch.device('cuda')
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))

else:
    print('No GPU available, using the CPU instead.')
    device = torch.device('cpu')


def get_args(parser):
    parser.add_argument(
        '-clamp_model_name',
        type=str,
        default='sander-wood/clamp-small-512',
        help='The CLaMP model name, either "sander-wood/clamp-small-512" or "sander-wood/clamp-small-1024"',
    )
    parser.add_argument(
        '-input_dir',
        type=Path,
        help='Input directory with .abc files',
        required=True,
    )
    parser.add_argument(
        '-output_dir',
        type=Path,
        help='Output directory',
        required=True,
    )

    return parser


# parse arguments

CLAMP_MODEL_NAME = 'sander-wood/clamp-small-512'
BATCH_SIZE = 16

# load CLaMP model
model = CLaMP.from_pretrained(CLAMP_MODEL_NAME)
music_length = model.config.max_length
model = model.to(device)
model.eval()

# initialize patchilizer
patchilizer = MusicPatchilizer()


def encoding_data(data):
    """
    Encode the data into ids

    Args:
        data (list): List of strings

    Returns:
        ids_list (list): List of ids
    """
    ids_list = []
    for item in data:
        patches = patchilizer.encode(item, music_length=music_length, add_eos_patch=True)
        ids_list.append(torch.tensor(patches).reshape(-1))

    return ids_list


def abc_filter(lines):
    """
    Filter out the metadata from the abc file

    Args:
        lines (list): List of lines in the abc file

    Returns:
        music (str): Music string
    """
    music = ''
    for line in lines:
        if (
            line[:2] in ['A:', 'B:', 'C:', 'D:', 'F:', 'G', 'H:', 'N:', 'O:', 'R:', 'r:', 'S:', 'T:', 'W:', 'w:', 'X:', 'Z:']
            or line == '\n'
            or (line.startswith('%') and not line.startswith('%%score'))
        ):
            continue
        else:
            if '%' in line and not line.startswith('%%score'):
                line = '%'.join(line.split('%')[:-1])
                music += line[:-1] + '\n'
            else:
                music += line + '\n'
    return music


def load_music(filename):
    """
    Load the music from the xml file

    Args:
        filename (str): Path to the xml file

    Returns:
        music (str): Music string
    """
    text = None
    with open(filename, 'r') as f:
        text = f.read()
    output = text.replace('\r', '')
    music = unidecode(output).split('\n')
    music = abc_filter(music)

    return music


def get_features(ids_list):
    """
    Get the features from the CLaMP model

    Args:
        ids_list (list): List of ids

    Returns:
        features_list (torch.Tensor): Tensor of features with a shape of (batch_size, hidden_size)
    """
    features_list = []
    print('Extracting music features...')
    with torch.no_grad():
        for ids in tqdm(ids_list):
            ids = ids.unsqueeze(0)
            masks = torch.tensor([1] * (int(len(ids[0]) / PATCH_LENGTH))).unsqueeze(0)
            features = model.music_enc(ids, masks)['last_hidden_state']
            features = model.avg_pooling(features, masks)
            features = model.music_proj(features)
            features_list.append(features[0])

    return torch.stack(features_list).to(device)


def main(input_dir: Path, output_dir: Path, batch_size: int):
    all_srcs = list(input_dir.glob('**/*.abc'))
    assert len(all_srcs) != 0

    for start_idx in range(0, len(all_srcs), batch_size):
        queries = []
        srcs = all_srcs[start_idx : start_idx + batch_size]
        for src in srcs:
            query = load_music(src)
            queries.append(unidecode(query))
        dsts = [output_dir.joinpath(*src.parts[len(input_dir.parts) : -1]).joinpath(f'{src.stem}.json') for src in srcs]

        # encode query
        query_ids = encoding_data(queries)
        query_features = get_features(query_ids)

        for dst, query_feature in zip(dsts, query_features):
            dst.unlink(missing_ok=True)
            dst.parent.mkdir(parents=True, exist_ok=True)
            with open(dst, 'tw') as f:
                dump(query_feature.tolist(), f)


if __name__ == '__main__':
    args = get_args(argparse.ArgumentParser()).parse_args()
    main(args.input_dir, args.output_dir, BATCH_SIZE)
