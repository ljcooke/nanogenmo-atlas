import random

from .types import RandomStack, XmlCorpus
from .util import sphere_surface_area
from .util import titlecase


EXOPLANET_CORPUS = 'data/oec-systems.xml'

EARTH_RADIUS_KM = 6371.0
JUPITER_RADIUS_KM = 69911.0

EARTH_SURFACE_KM2 = sphere_surface_area(EARTH_RADIUS_KM)
EARTH_LAND_SURFACE_KM2 = EARTH_SURFACE_KM2 * 0.292


EPOCH = 2500
LATEST_SETTLED = 3200
EARTH_POPULATION_MAX = 12e9


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

        # convert the radius from Jupiter radii to km
        radius = self.xml.find('radius')
        try:
            self.jupiter_radii = float(radius.text)
            self.radius = self.jupiter_radii * JUPITER_RADIUS_KM
            self.earth_radii = self.radius / EARTH_RADIUS_KM
        except (AttributeError, TypeError):
            self.radius = 0.0
            return

        self.surface_area = sphere_surface_area(self.radius)

        # how much of the surface is habitable
        self.habitable_ratio = random.randint(5, 95) * 0.01

        # simple population model: generate a random population of Earth,
        # then scale it according to the land surface area of the planet
        earth_max = EARTH_POPULATION_MAX
        earth_pop = random.randint(int(earth_max * 0.001), earth_max)
        surface = self.surface_area * self.habitable_ratio
        self.population = earth_pop * (surface / EARTH_LAND_SURFACE_KM2)

    def __bool__(self):
        return self.radius > 0.0 and self.population > 1


class Star(Entity):

    def __init__(self, xml, system):
        super().__init__(xml)

        self.system = system

        planets = (Planet(node, self) for node in xml.findall('.//planet'))
        self.planets = tuple(p for p in planets if p)

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
        radius_counts = []
        years_settled = []

        for system in self.systems:
            star_counts.append(len(system.stars))
            years_settled.append(system.year_settled)

            for star in system.stars:
                planet_counts.append(len(star.planets))

                for planet in star.planets:
                    radius_counts.append(planet.radius)

        total_stars, total_planets = sum(star_counts), sum(planet_counts)

        print('OPEN EXOPLANET CATALOGUE')
        print('')
        print('Total Systems:    %9d.' % total_systems)
        print('Total Stars:      %9d.' % total_stars)
        print('Total Planets:    %9d.' % total_planets)
        print('')
        print('Minimum Stars:    %9d.' % min(star_counts))
        print('Maximum Stars:    %9d.' % max(star_counts))
        print('Average Stars:    %14.4f' % (float(total_stars) / len(star_counts)))
        print('')
        print('Minimum Planets:  %9d.' % min(planet_counts))
        print('Maximum Planets:  %9d.' % max(planet_counts))
        print('Average Planets:  %14.4f' % (float(total_planets) / len(planet_counts)))
        print('')
        print('Minimum Radius:   %14.4f km' % min(radius_counts))
        print('Maximum Radius:   %14.4f km' % max(radius_counts))
        print('Average Radius:   %14.4f km' % (sum(radius_counts) / len(radius_counts)))
        print('Earth Radius:     %14.4f km' % EARTH_RADIUS_KM)
        print('Jupiter Radius:   %14.4f km' % JUPITER_RADIUS_KM)
        print('')
        print('Earliest Settled: %9d CE' % min(years_settled))
        print('Latest Settled:   %9d CE' % max(years_settled))
