#!/usr/bin/env python

import argparse

from functioneer import Functioneer
from output import Outputer
from commenter import Commenter
from linenamer import Linenamer
from iffer import Iffer
from macroer import Macroer
import util


def main():
    args = parse()

    # strip comments
    #text = Commenter(load(args.file)).comments_removed()

    text = load(args.file)

    if args.macrosFile:
        text = Macroer(text, args.macrosFile).replaceMacros()
    else:
        text = Macroer(text, None).replaceMacros()

    text2 = []
    for ll in text:
        if util.real_strip(ll) != '':
            text2.append(util.real_strip(ll))
    text = text2

    text = Linenamer(text).linesnames_changed()

    #text = util.filter_lines(text)

    # replace if statements
    iffer = Iffer(text)
    ifs = 0
    iffer.parse()

    text = iffer.lines

    # replace functions
    functioneer = Functioneer(text)
    functioneer.get_functions()

    outer = Outputer(functioneer, iffer)
    print outer.out()


def parse():
    parser = argparse.ArgumentParser('compile lm')
    parser.add_argument('--file', required=True)
    parser.add_argument('--macrosFile')
    return parser.parse_args()


def load(filename):
    with open(filename, 'r') as ff:
        return ff.readlines()


if __name__ == "__main__":
    main()
