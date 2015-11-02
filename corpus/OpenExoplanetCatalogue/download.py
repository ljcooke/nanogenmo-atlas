#!/usr/bin/env python3
import gzip
import hashlib
import io
import os
import shutil
import sys
import urllib.request

FILENAME = 'systems.xml'
BACKUP_FILENAME = FILENAME + '~'
URL = 'https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz'

KIBI = 1024
MEBI = KIBI * 1024

def bytesize(numbytes):
    if numbytes == 1:
        return '1 byte'
    elif numbytes < KIBI:
        return '%d bytes' % numbytes
    elif numbytes < MEBI:
        return '%0.2f KiB' % (numbytes / KIBI)

def main():
    exists = os.path.isfile(FILENAME)

    if exists:
        with open(FILENAME, 'rb') as fp:
            oldhash = hashlib.sha224(fp.read()).hexdigest()
    else:
        oldhash = None

    print('Downloading {}'.format(URL))
    res = urllib.request.urlopen(URL).read()
    if not res:
        sys.stdout.write('Error: Downloaded 0 bytes\n')
        return 1

    print('Uncompressing {}'.format(bytesize(len(res))))
    xml = gzip.GzipFile(fileobj=io.BytesIO(res)).read()
    print('Uncompressed size: {}'.format(bytesize(len(xml))))

    newhash = hashlib.sha224(xml).hexdigest()
    if oldhash == newhash:
        print('No change')
        return

    if exists:
        print('Moving old data to {}'.format(BACKUP_FILENAME))
        shutil.move(FILENAME, BACKUP_FILENAME)

    print('Saving new data to {}'.format(FILENAME))
    with open(FILENAME, 'wb') as fp:
        fp.write(xml)

if __name__ == '__main__':
    sys.exit(main())
