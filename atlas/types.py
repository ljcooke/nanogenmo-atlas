import random

from xml.etree import ElementTree


class Corpus:

    def __init__(self, filename):
        self.filename = filename


class XmlCorpus(Corpus):

    def __init__(self, filename):
        super().__init__(filename)
        with open(filename, encoding='utf-8') as fp:
            self.tree = ElementTree.parse(fp)

    def findall(self, match):
        return self.tree.findall(match)


class RandomStack:

    def __init__(self, items):
        items = list(items)
        random.shuffle(items)
        self.unseen = items
        self.seen = []

    def __len__(self):
        return len(self.unseen)

    def pop(self):
        # raises IndexError if no more stars or binaries
        child = self.unseen.pop()
        self.seen.append(child)
        return child
