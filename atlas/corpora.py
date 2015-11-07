import json
import os
from glob import glob


DATA_DIR = 'data/corpora/data'


def load_json(filename):
    path = os.path.join(DATA_DIR, filename) + '.json'
    with open(path, encoding='utf-8') as fp:
        return json.load(fp)

def load(filename, key=None):
    vocab = load_json(filename)
    key = key or os.path.basename(filename)
    return vocab[key]


def planet_names():
    names = []

    names += load('mythology/greek_gods')
    names += load('mythology/greek_titans')
    names += load('plants/flowers')

    names += [spell['incantation'] for spell in load('words/spells')]

    many = load('mythology/norse_gods', key='norse_deities')
    names += many['gods'] + many['goddesses']

    return set(filter(bool,
                      (name.split()[0] for name in names)))


if __name__ == '__main__':
    print(planet_names())
