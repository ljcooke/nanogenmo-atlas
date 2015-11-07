from . import corpora
from . import oec
from .types import RandomStack


DEFAULT_NUM_CHAPTERS = 50


class Chapter:

    def __init__(self, number, planet, name):
        self.planet = planet
        self.human_name = name
        self.sci_name = planet.name
        self.title = '{} ({})'.format(self.human_name, self.sci_name)


class Story:

    def __init__(self, num_chapters=DEFAULT_NUM_CHAPTERS):
        self.exoplanets = oec.Exoplanets()

        planet_names = RandomStack(corpora.planet_names())

        systems = self.exoplanets.stack()
        chapters = []
        for i in range(1, num_chapters + 1):
            system = systems.pop()
            star = system.random_star()
            planet = star.random_planet()
            name = planet_names.pop()
            chapters.append(Chapter(i, planet, name))
        self.chapters = chapters

    def contents(self):
        for i, chapter in enumerate(self.chapters):
            yield (i + 1, chapter.title)
