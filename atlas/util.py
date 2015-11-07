import locale
import math
import textwrap


DEFAULT_TEXT_WIDTH = 78


def sphere_surface_area(radius):
    return 4.0 * math.pi * (radius ** 2)


def titlecase(text):
    return ' '.join(t.capitalize() for t in text.split())

def wrap(text, width=DEFAULT_TEXT_WIDTH, indent=''):
    return textwrap.fill(text, width,
                         initial_indent=indent,
                         subsequent_indent=indent,
                         break_long_words=False,
                         break_on_hyphens=False)


MEGA = 1000 * 1000
GIGA = MEGA * 1000
TERA = GIGA * 1000

def human_num(num):
    grouped = lambda n: locale.format('%0.1f', n, grouping=True)
    if num < MEGA * 0.85:
        return grouped(num)
    elif num < GIGA * 0.85:
        return '%s million' % grouped(num / MEGA)
    elif num < TERA * 0.85:
        return '%s billion' % grouped(num / GIGA)
    else:
        return '%s trillion' % grouped(num / TERA)
