#!/usr/bin/env python

import argparse

from functioneer import Functioneer
from output import Outputer
from commenter import Commenter
from iffer import Iffer
import util


def main():
    args = parse()

    # strip comments
    text = Commenter(load(args.file)).comments_removed()

    text = util.filter_lines(text)

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
    return parser.parse_args()


def load(filename):
    with open(filename, 'r') as ff:
        return ff.readlines()


if __name__ == "__main__":
    main()
