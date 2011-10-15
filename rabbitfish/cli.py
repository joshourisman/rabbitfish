#!/usr/bin/env python
import sys

from optparse import OptionParser

from jug import generatesite

VERSION = "0.1a"


def main():
    print("One dead, unjugged rabbitfish later...", file=sys.stderr)
    usage = "usage: %prog ACTION"
    version = "%prog {}".format(VERSION)

    parser = OptionParser(prog='rabbitfish',
                          usage=usage,
                          version=version)

    options, args = parser.parse_args()

    ACTIONS = {
        'generatesite': generatesite,
        }

    try:
        action = args[0]
    except IndexError:
        parser.print_usage()
        return

    if action not in ACTIONS:
        parser.print_usage()
        print('{} is not a supported action.'.format(action), file=sys.stderr)
        print('Supported actions include: {}'.format(' ,'.join(ACTIONS)),
              file=sys.stderr)
        return

    ACTIONS[action]()

if __name__ == "__main__":
    main()
