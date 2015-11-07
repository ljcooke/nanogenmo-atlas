#!/usr/bin/env python3
"""
ATLAS OF REMOTE PLANETS
A NaNoGenMo story by Liam Cooke, Nov 2015

"""
import argparse
import os
import sys

from . import oec, story


PREREQUISITES = (oec.EXOPLANET_CORPUS, )


def print_stats():
    divider = '=' * 78

    print(divider)
    exoplanets = oec.Exoplanets()
    exoplanets.print_stats()
    print(divider)

def check_exists(path):
    if os.path.exists(path):
        return True
    else:
        sys.stderr.write('Error: Could not find {}\n'.format(path))

def check_prerequisites():
    if all(check_exists(fn) for fn in PREREQUISITES):
        return True
    else:
        sys.stderr.write('Please run ./bootstrap.sh\n')

def main():
    if not check_prerequisites():
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('generate', 'stats'))
    parser.add_argument('-c', '--chapters', type=int,
                        default=story.DEFAULT_NUM_CHAPTERS)

    if not sys.argv[1:]:
        parser.print_help()
        return 1

    args = parser.parse_args()

    if args.action == 'generate':
        atlas = story.Story(num_chapters=args.chapters)
        for number, title in atlas.contents():
            print('{}. {}'.format(number, title))
    elif args.action == 'stats':
        print_stats()
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
