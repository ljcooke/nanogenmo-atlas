import sys

from . import corpora
from . import oec
from .types import RandomStack
from .util import titlecase


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
        self.planet = planet
        self.human_name = name
        self.sci_name = planet.name
        self.title = '{} ({})'.format(self.human_name, self.sci_name)


class Story:

    def __init__(self, num_chapters=DEFAULT_NUM_CHAPTERS):
        self.exoplanets = oec.Exoplanets()

        systems = self.exoplanets.stack()
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

    def contents(self):
        for i, chapter in enumerate(self.chapters):
            yield (i + 1, chapter.title)
