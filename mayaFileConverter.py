#! /usr/bin/env python2

# Copyright (c) 2013 ILMVFX Blog All rights reserved. Used under
# authorization. This material contains the confidential and proprietary
# information of the company. and may not be copied in whole or in part
# without the express written permission of the company. This copyright
# notice does not imply publication.

__author__ = "Jiang Han"
__copyright__ = "Copyright 2013, The ShittyTools Project"
__credits__ = ["Jiang Han"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "oglop"
__email__ = "oglops@gmail.com"
__website__ = 'ilmvfx.wordpress.com'
__status__ = "Shitty"

import os
import argparse
import re


def newName(f, args):
    dir = os.path.dirname(f)
    name, ext = os.path.splitext(f)
    ver = args.v
    newName = '{name}_{ver}'.format(**locals())
    return '{newName}{ext}'.format(**locals())


def main(args=None):

    for f in args.files:
        newFile = newName(f, args)

        if f.endswith('.mb'):
            with open(f, "rb") as mbFile:
                m = mbFile.read()
                verEndPos = m.find('UVER')
                currentVer = m[0x20:verEndPos]
                if currentVer != args.v:

                    print f, '-->', newFile
                    m = m.replace(bytes(currentVer), bytes(args.v), 1)

                    with open(newFile, "wb") as newFile:
                        newFile.write(m)
                else:
                    print f, '-->', 'skipped'

        elif f.endswith('.ma'):

            with open(f, "r") as maFile:
                with open(newFile, "w") as newMaFile:
                    for line in maFile:

                        if re.match('^requires maya ".*";\n', line):
                            currentVer = line.split('"')[1]
                            if currentVer != args.v:
                                print f, '-->', newFile
                                line = line.replace(currentVer, args.v, 1)
                                newMaFile.write(line)
                                break
                            else:
                                print f, '-->', 'skipped'

                        newMaFile.write(line)

                    # we have replaced the line
                    for line in maFile:
                        newMaFile.write(line)



def _parseArgs():

    parser = argparse.ArgumentParser(
        description='MayaFileConverter - a shitty script to convert maya file version')
    parser.add_argument('-v', help='target scene file version',
                        nargs='?', required=False)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    return args


def run():
    args = _parseArgs()
    # print args
    main(args)

if __name__ == '__main__':
    run()
