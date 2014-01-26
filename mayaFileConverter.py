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
__website__ = 'https://ilmvfx.wordpress.com'
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


def getVerBase(ver):
    verBase = re.search('^\d+', ver).group()
    return int(verBase)


def main(args=None):

    for f in args.files:
        newFile = newName(f, args)

        if f.endswith('.mb'):

            chunk = 1024
            with open(f, "rb") as mbFile:
                with open(newFile, "wb") as newMbFile:

                    m = mbFile.read(chunk)

                    verEndPos = m.find('UVER')

                    currentVer = m[verEndPos - 8:verEndPos]
                    print 'currentVer [%s]' % currentVer
                    if currentVer != args.v:

                        print f, '-->', newFile

                        newMbFile.write(m[:verEndPos - 8])
                        newMbFile.write(args.v)

                        for i in range(8 - len(args.v)):
                            newMbFile.write(b'\x00')

                        newMbFile.write(m[verEndPos:])

                        chunk = 1024 * 1024
                        while True:
                            piece = mbFile.read(chunk)
                            if not piece:
                                print 'last run:', piece
                                break
                            newMbFile.write(piece)

                    else:
                        print f, '-->', 'skipped'

        elif f.endswith('.ma'):

            with open(f, "r") as maFile:
                with open(newFile, "w") as newMaFile:
                    verChange = False
                    for line in maFile:

                        if re.match('^requires maya ".*";\n', line):
                            currentVer = line.split('"')[1]
                            if currentVer != args.v:
                                print f, '-->', newFile
                                line = line.replace(currentVer, args.v, 1)
                                newMaFile.write(line)
                                verChange = True
                                break
                            else:
                                print f, '-->', 'skipped'

                        newMaFile.write(line)

                    # real scene content starts somewhere below this "requires
                    # xxx" line of course

                    hack = False
                    if verChange:
                        fileVer = getVerBase(currentVer)
                        newVer = getVerBase(args.v)
                        if fileVer > newVer and fileVer > 2012:
                            hack = True

                    # we have replaced the version line
                    if verChange and hack:
                        for line in maFile:

                            # this is for the -ch fix
                            # // Error: file: E:/shittyTools/2014_cube_2012.ma line 94: Invalid flag '-ch' //
                            if re.match('\tsetAttr.*-ch \d+ .*', line):
                                line = re.sub(' -ch \d+', '', line)

                            newMaFile.write(line)
                    # we have nothing to deal with, just write everything
                    else:
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
