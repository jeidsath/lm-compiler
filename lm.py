#!/usr/bin/env python

import argparse

from functioneer import Functioneer
from output import Outputer


def parse():
    parser = argparse.ArgumentParser('compile lm')
    parser.add_argument('--file', required=True)
    return parser.parse_args()


def load(filename):
    with open(filename, 'r') as ff:
        return ff.readlines()


def output(fns):
    lines = []
    for fn in fns:
        for xx, ll in enumerate(fn['lines']):
            app = ""
            if xx == 0:
                app = ";FN:" + fn['name']
            lines.append(ll + app)
        lines.append('RTN')
    return lines


def main():
    args = parse()
    functioneer = Functioneer(load(args.file))
    functioneer.get_functions()
    outer = Outputer(functioneer)
    print outer.out()

if __name__ == "__main__":
    main()
