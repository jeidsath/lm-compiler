#!/usr/bin/env python

import argparse

from functioneer import Functioneer
from output import Outputer
from commenter import Commenter


def main():
    args = parse()

    # strip comments
    text = Commenter(load(args.file)).comments_removed()

    # replace functions
    functioneer = Functioneer(text)
    functioneer.get_functions()

    outer = Outputer(functioneer)
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
