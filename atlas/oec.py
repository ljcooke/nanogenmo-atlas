import random

from .types import RandomStack, XmlCorpus
from .util import titlecase


EXOPLANET_CORPUS = 'data/oec-systems.xml'

EPOCH = 2500
LATEST_SETTLED = 3200


class Entity:

    def __init__(self, xml):
        self.xml = xml
        self.names = tuple(node.text for node in xml.findall('name'))

    @property
    def name(self):
        return titlecase(self.names[0])

    @property
    def long_name(self):
        return titlecase(self.names[-1])


class Planet(Entity):

    def __init__(self, xml, star):
        super().__init__(xml)

        self.star = star


class Star(Entity):

    def __init__(self, xml, system):
        super().__init__(xml)

        self.system = system
        self.planets = tuple(Planet(node, self)
                             for node in xml.findall('.//planet'))

    def random_planet(self):
        return random.choice(self.planets)

    def __bool__(self):
        return any(self.planets)


class System(Entity):

    def __init__(self, xml):
        super().__init__(xml)

        children = []
        for node in xml.findall('.//star'):
            star = Star(node, self)
            if star:
                children.append(star)
        for node in xml.findall('.//binary'):
            pass  # TODO
        self.stars = tuple(children)

        distance = self.xml.find('distance')
        try:
            parsecs = float(distance.text)
            par_minus = float(distance.attrib.get('errorminus') or 0)
            par_plus = float(distance.attrib.get('errorplus') or 0)
            ly_min = (parsecs - par_minus) / 3.26156
            ly_max = (parsecs + par_plus) / 3.26156
            # TODO: use ly_min and ly_max for random variance
            ly = (ly_min + ly_max) * 0.5
            self.year_settled = int(EPOCH + random.randint(1, 100) + ly)
            if self.year_settled > LATEST_SETTLED:
                self.year_settled = 0
        except AttributeError:
            self.year_settled = 0

    def random_star(self):
        return random.choice(self.stars)

    def __bool__(self):
        return bool(self.stars and self.year_settled)


class Exoplanets(XmlCorpus):
    """
    Open Exoplanet Catalogue

    """
    def __init__(self, filename=EXOPLANET_CORPUS):
        super().__init__(filename)

        systems = []
        for node in self.findall('.//system'):
            system = System(node)
            if system:
                systems.append(system)
        self.systems = tuple(systems)

    def stack(self):
        """Get a randomly-sorted stack of systems."""
        return RandomStack(self.systems)

    def print_stats(self):
        total_systems = len(self.systems)
        star_counts, planet_counts = [], []
        years_settled = []

        for system in self.systems:
            star_counts.append(len(system.stars))
            years_settled.append(system.year_settled)

            for star in system.stars:
                planet_counts.append(len(star.planets))

        total_stars, total_planets = sum(star_counts), sum(planet_counts)

        print('OPEN EXOPLANET CATALOGUE')
        print('')
        print('Total Systems:     %8d.' % total_systems)
        print('Total Stars:       %8d.' % total_stars)
        print('Total Planets:     %8d.' % total_planets)
        print('')
        print('Minimum Stars:     %8d.' % min(star_counts))
        print('Maximum Stars:     %8d.' % max(star_counts))
        print('Average Stars:     %13.4f' % (float(total_stars) / len(star_counts)))
        print('')
        print('Minimum Planets:   %8d.' % min(planet_counts))
        print('Maximum Planets:   %8d.' % max(planet_counts))
        print('Average Planets:   %13.4f' % (float(total_planets) / len(planet_counts)))
        print('')
        print('Earliest Settled:  %8d CE' % min(years_settled))
        print('Latest Settled:    %8d CE' % max(years_settled))
