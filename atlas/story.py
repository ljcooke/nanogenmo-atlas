import locale
import os
import sys
from itertools import chain

from . import corpora
from . import oec
from .render import RENDERERS
from .types import RandomStack
from .util import titlecase


TITLE = 'Atlas of Remote Planets'
DEFAULT_NUM_CHAPTERS = 50


def planet_names():
    names = []

    names += corpora.load('mythology/greek_gods')
    names += corpora.load('mythology/greek_titans')
    names += corpora.load('plants/flowers')

    names += [spell['incantation']
              for spell in corpora.load('words/spells')]

    many = corpora.load('mythology/norse_gods', key='norse_deities')
    names += many['gods'] + many['goddesses']

    return set(filter(bool,
                      (titlecase(name.split()[0]) for name in names)))


class Chapter:

    def __init__(self, number, planet, name):
        self.number = number
        self.slug = 'ch{}'.format(number)
        self.planet = planet
        self.human_name = name
        self.sci_name = planet.name
        self.title = '{} ({})'.format(self.human_name, self.sci_name)
        self.paragraphs = [' '.join(['meow'] * 200).capitalize() + '.'] * 5

    def __iter__(self):
        return iter(self.paragraphs)

    def __len__(self):
        words = chain.from_iterable(p.split() for p in self.paragraphs)
        return sum(1 for w in words if len(w) > 1)


class Story:

    def __init__(self, num_chapters=DEFAULT_NUM_CHAPTERS):
        self.title = TITLE

        exoplanets = oec.Exoplanets()
        systems = exoplanets.stack()
        names = RandomStack(planet_names())

        chapters = []
        for i in range(1, num_chapters + 1):
            try:
                system = systems.pop()
                name = names.pop()
            except IndexError:
                sys.stderr.write('Warning: Reached a maximum of {} chapters.\n'
                                 .format(i - 1))
                break
            star = system.random_star()
            planet = star.random_planet()
            chapters.append(Chapter(i, planet, name))
        self.chapters = chapters

    def __iter__(self):
        return iter(self.chapters)

    def __len__(self):
        return sum(len(ch) for ch in self.chapters)

    def contents(self):
        for i, chapter in enumerate(self.chapters):
            yield (i + 1, chapter.title)

    def print_stats(self):
        print('GENERATED STORY')
        print('')
        print('Chapter Count:     %8d.' % len(self.chapters))
        print('Word Count:        %8d.' % len(self))

    def render_in_dir(self, dirname):
        print('Word count: {}'.format(len(self)))

        if not os.path.isdir(dirname):
            print('Creating directory: {}'.format(dirname))
            os.mkdir(dirname)

        for cls in RENDERERS:
            renderer = cls(story=self)
            renderer.render_file(dirname)
