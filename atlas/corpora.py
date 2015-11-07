import json
import os


DATA_DIR = 'data/corpora/data'


def load_json(filename):
    path = os.path.join(DATA_DIR, filename) + '.json'
    with open(path, encoding='utf-8') as fp:
        return json.load(fp)

def load(filename, key=None):
    vocab = load_json(filename)
    key = key or os.path.basename(filename)
    return vocab[key]
